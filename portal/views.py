from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, reverse
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .forms import AskForm, AnswerForm, CommentForm
from .models import Question, Candidate, Comment
from django.db.models import Q
from . import choices


class UpvoteAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Question, pk=pk)
        user = self.request.user
        updated = False
        upvote = 0
        downvote = 0
        upvoteColor = "black"
        downvoteColor = "black"
        if user.is_authenticated:
            updated = True
            if user.junta in obj.upvotes.all():
                obj.upvotes.remove(user.junta)
                upvote = -1
            else:
                if user.junta in obj.downvotes.all():
                    obj.downvotes.remove(user.junta)
                    downvote = -1
                obj.upvotes.add(user.junta)
                upvoteColor = "blue"
                upvote = 1

        data = {
            'updated': updated,
            'upvote': upvote,
            'downvote': downvote,
            'upvoteColor': upvoteColor,
            'downvoteColor': downvoteColor
        }
        return Response(data)


class DownvoteAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Question, pk=pk)
        user = self.request.user
        updated = False
        upvote = 0
        downvote = 0
        upvoteColor = "black"
        downvoteColor = "black"
        if user.is_authenticated:
            updated = True
            if user.junta in obj.downvotes.all():
                obj.downvotes.remove(user.junta)
                downvote = -1
            else:
                if user.junta in obj.upvotes.all():
                    obj.upvotes.remove(user.junta)
                    upvote = -1
                obj.downvotes.add(user.junta)
                downvoteColor = "red"
                downvote = 1

        data = {
            'updated': updated,
            'upvote': upvote,
            'downvote': downvote,
            'upvoteColor': upvoteColor,
            'downvoteColor': downvoteColor
        }
        return Response(data)


class UpvoteAPIToggleComment(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Comment, pk=pk)
        user = self.request.user
        updated = False
        upvote = 0
        downvote = 0
        upvoteColor = "black"
        downvoteColor = "black"
        if user.is_authenticated:
            updated = True
            if user.junta in obj.upvotes.all():
                obj.upvotes.remove(user.junta)
                upvote = -1
            else:
                if user.junta in obj.downvotes.all():
                    obj.downvotes.remove(user.junta)
                    downvote = -1
                obj.upvotes.add(user.junta)
                upvoteColor = "blue"
                upvote = 1

        data = {
            'updated': updated,
            'upvote': upvote,
            'downvote': downvote,
            'upvoteColor': upvoteColor,
            'downvoteColor': downvoteColor
        }
        return Response(data)


class DownvoteAPIToggleComment(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Comment, pk=pk)
        user = self.request.user
        updated = False
        upvote = 0
        downvote = 0
        upvoteColor = "black"
        downvoteColor = "black"
        if user.is_authenticated:
            updated = True
            if user.junta in obj.downvotes.all():
                obj.downvotes.remove(user.junta)
                downvote = -1
            else:
                if user.junta in obj.upvotes.all():
                    obj.upvotes.remove(user.junta)
                    upvote = -1
                obj.downvotes.add(user.junta)
                downvoteColor = "red"
                downvote = 1

        data = {
            'updated': updated,
            'upvote': upvote,
            'downvote': downvote,
            'upvoteColor': upvoteColor,
            'downvoteColor': downvoteColor
        }
        return Response(data)


class ApproveAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Question, pk=pk)
        user = self.request.user
        updated = False
        if user.is_authenticated:
            if user.junta.role == choices.ELECTION_COMMISSION:
                if not obj.approved:
                    updated = True
                    obj.approved = True
                    obj.approved_by = user.junta
                    obj.save()
        data = {
            'updated': updated,
        }
        return Response(data)


class ApproveAPIToggleComment(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Comment, pk=pk)
        user = self.request.user
        updated = False
        if user.is_authenticated:
            if user.junta.role == choices.ELECTION_COMMISSION:
                if not obj.approved:
                    updated = True
                    obj.approved = True
                    obj.approved_by = user.junta
                    obj.save()
        data = {
            'updated': updated,
        }
        return Response(data)


class DeleteQuestionAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Question, pk=pk)
        user = self.request.user
        updated = False
        if user.is_authenticated:
            if user.junta.role == choices.ELECTION_COMMISSION:
                updated = True
                for comment in obj.comments.all():
                    comment.delete()
                obj.delete()
        data = {
            'updated': updated,
        }
        return Response(data)


class DeleteCommentAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Comment, pk=pk)
        user = self.request.user
        updated = False
        if user.is_authenticated:
            if user.junta.role == choices.ELECTION_COMMISSION:
                updated = True
                obj.delete()
        data = {
            'updated': updated,
        }
        return Response(data)


def index(request):
    question_form = AskForm()
    comment_form = CommentForm()
    d = {'question_form': question_form, 'comment_form': comment_form}
    if request.user.is_authenticated:
        d['is_authenticated'] = True
        user = request.user.junta
        d['user'] = user
        if user.role == choices.ELECTION_COMMISSION:
            unapproved_questions = Question.objects.filter(approved=False).order_by('-asked_on')
            unapproved_comments = Comment.objects.filter(approved=False).order_by('-commented_on')
            approved_questions = Question.objects.filter(approved=True).order_by('-asked_on')
            d['unapproved_questions'] = unapproved_questions
            d['unapproved_comments'] = unapproved_comments
            d['role'] = 'admin'
        elif user.role == choices.CANDIDATE:
            approved_questions = Question.objects.filter(approved=True)\
                                                 .filter(~Q(asked_to=request.user.junta.candidate.all()[0]))\
                                                 .order_by('-asked_on')
            my_questions = Question.objects.filter(asked_to=request.user.junta.candidate.all()[0])\
                                           .filter(approved=True)\
                                           .order_by('-asked_on')
            print(my_questions)
            d['my_questions'] = my_questions
        else:
            approved_questions = Question.objects.filter(approved=True).order_by('-asked_on')
    else:
        approved_questions = Question.objects.filter(approved=True).order_by('-asked_on')
    d['approved_questions'] = approved_questions
    if request.method == 'POST':
        if d['is_authenticated']:
            questionForm = AskForm(request.POST)
            if questionForm.is_valid():
                question = questionForm.save(commit=False)
                question.asked_by = request.user.junta
                question.save()
                questionForm.save_m2m()
                pass
            else:
                print(questionForm.errors)
            return HttpResponseRedirect(reverse('portal:index'))
        else:
            return HttpResponseRedirect(reverse('portal:login'))

    return render(request, 'index.html', d)


def load_candidates(request):
    position = request.GET.get('position')
    candidates = Candidate.objects.filter(position=position)
    return render(request, 'candidates_dropdown_list.html', {'candidates': candidates})


def sort_questions(request):
    order_by = request.GET.get('order_by')
    question_type = request.GET.get('question_type')
    candidate = request.GET.get('candidate')

    questions = None

    if question_type == 'unapproved':
        questions = Question.objects.filter(approved=False)
    elif candidate == choices.VOTER:
        questions = Question.objects.filter(approved=True)
    else:
        if question_type == 'my':
            questions = Question.objects.filter(asked_to=request.user.junta.candidate.all()[0])
        else:
            questions = Question.objects.filter(asked_to=~Q(request.user.junta.candidate.all()[0]))

    if order_by == 'recent':
        questions = questions.order_by('-asked_on')
    else:
        questions = questions.order_by('upvotes')


def answer_view(request, pk):
    question = Question.objects.get(pk=pk)
    answer_form = AnswerForm()
    if question.answered:
        answer_form = AnswerForm({'answer': question.answer})

    d = {'question': question, 'answer_form': answer_form}

    if request.user.is_authenticated:
        d['is_authenticated'] = True

    if request.POST:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            question.answer = answer
            question.answered = True
            question.answered_on = timezone.now()
            question.save()
        else:
            print("AnswerForm POST Error: ", form.errors)
        return HttpResponseRedirect(reverse('portal:index'))

    return render(request, 'answer.html', d)


def comment_view(request, pk):
    question = Question.objects.get(pk=pk)
    comment_form = CommentForm()

    d = {'question': question, 'comment_form': comment_form}

    if request.user.is_authenticated:
        d['is_authenticated'] = True

    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment_by = request.user.junta
            comment.question = question
            comment.comment = form.cleaned_data['comment']
            comment.commented_on = timezone.now()
            comment.save()
            form.save_m2m()
            pass
        else:
            print("CommentForm POST Error: ", form.errors)
        return HttpResponseRedirect(reverse('portal:index'))

    return render(request, 'comment.html', d)


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('portal:index'))
            else:
                return HttpResponse("Account not active")
        else:
            print("Wrong: {} {}".format(username, password))
            return HttpResponse("Invalid Login Details")
    else:
        return render(request, 'login.html')


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("portal:index"))
