from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone

from . import choices


class Junta(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='junta')
    profile_pic = models.ImageField(blank=True)
    role = models.CharField(max_length=32, choices=choices.ROLES_CHOICES, default=choices.VOTER)

    def image_tag(self):
        from django.utils.html import escape, format_html
        try:
            return format_html('<img src="%s" width="150" height="150"/>' % escape(self.profile_pic.url))
        except ValueError:
            return format_html('No profile pic')

    image_tag.short_description = user
    image_tag.allow_tags = True

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class Candidate(models.Model):
    user = models.ForeignKey(Junta, on_delete=models.CASCADE, related_name='candidate')
    bio = models.TextField(blank=True)
    position = models.CharField(max_length=64, choices=choices.POSITION_CHOICES, default=choices.VP)
    videos = models.FileField(blank=True)
    agenda = models.FileField(blank=True)
    key_points = models.TextField(blank=True)

    def __str__(self):
        return '{} {}'.format(self.user.user.first_name, self.user.user.last_name)


class Question(models.Model):
    asked_by = models.ForeignKey(Junta, on_delete=models.CASCADE, related_name='questions_submitted')
    asked_to = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='question_asked')
    question = models.CharField(max_length=1024)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(Junta, on_delete=models.CASCADE, related_name='questions_approved', null=True)
    answer = models.TextField(blank=True)
    answered = models.BooleanField(default=False)
    asked_on = models.DateTimeField(blank=True)
    answered_on = models.DateTimeField(blank=True)
    upvotes = models.ManyToManyField(Junta, related_name='question_upvoted')
    downvotes = models.ManyToManyField(Junta, related_name='question_downvoted')

    class Meta:
        ordering = ['asked_on']

    @staticmethod
    def approve_questions(queryset):
        queryset.update(approved=True)

    def __str__(self):
        return '{}'.format(self.question)

    def get_absolute_url(self):
        return reverse("portal:question", kwargs={'pk': self.pk})

    def get_upvote_api_url(self):
        return reverse("portal:api-upvote", kwargs={'pk': self.pk})

    def get_downvote_api_url(self):
        return reverse("portal:api-downvote", kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.id:
            self.asked_on = timezone.now()
            self.answered_on = self.asked_on
        if len(self.answer) > 0 and self.answered:
            self.answered_on = timezone.now()

        return super(Question, self).save(*args, **kwargs)


class Comment(models.Model):
    comment_by = models.ForeignKey(Junta, on_delete=models.CASCADE, related_name='comments_submitted')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=1024, blank=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(Junta, on_delete=models.CASCADE, related_name='comments_approved', blank=True, null=True)
    commented_on = models.DateTimeField(blank=True)
    upvotes = models.ManyToManyField(Junta, related_name='comments_upvoted')
    downvotes = models.ManyToManyField(Junta, related_name='comments_downvoted')

    class Meta:
        ordering = ['commented_on']

    @staticmethod
    def approve_comments(queryset):
        queryset.update(approved=True)

    def __str__(self):
        return '{}'.format(self.comment)

    def get_absolute_url(self):
        return reverse("portal:comment", kwargs={'pk': self.pk})

    def get_upvote_api_url(self):
        return reverse("portal:api-upvote-comment", kwargs={'pk': self.pk})

    def get_downvote_api_url(self):
        return reverse("portal:api-downvote-comment", kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.id:
            self.commented_on = timezone.now()

        return super(Comment, self).save(*args, **kwargs)


class Hostel(models.Model):
    name = models.CharField(max_length=64)
    total_residents = models.IntegerField(default=0)
    no_of_votes = models.IntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.name)

