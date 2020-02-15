from django.urls import path, re_path
from django.views.generic import View

from .views import (
    index,
    user_login,
    user_logout,
    answer_view,
    comment_view,
    UpvoteAPIToggle,
    DownvoteAPIToggle,
    load_candidates,
    UpvoteAPIToggleComment,
    DownvoteAPIToggleComment,
    ApproveAPIToggle,
    ApproveAPIToggleComment,
    DeleteQuestionAPIToggle,
    DeleteCommentAPIToggle,
    # SortQuestionsAPI,
)

app_name = 'portal'

urlpatterns = [
    path('', index, name='index'),
    re_path('^(?P<pk>[0-9]+)/$', View.as_view(), name='question'),
    re_path('^api/(?P<pk>[0-9]+)/upvote/$', UpvoteAPIToggle.as_view(), name='api-upvote'),
    re_path('^api/(?P<pk>[0-9]+)/downvote/$', DownvoteAPIToggle.as_view(), name='api-downvote'),
    re_path('^api/(?P<pk>[0-9]+)/upvote-comment/$', UpvoteAPIToggleComment.as_view(), name='api-upvote-comment'),
    re_path('^api/(?P<pk>[0-9]+)/downvote-comment/$', DownvoteAPIToggleComment.as_view(), name='api-downvote-comment'),
    re_path('^(?P<pk>[0-9]+)/answer/$', answer_view, name='answer'),
    re_path('^(?P<pk>[0-9]+)/comment/$', comment_view, name='comment'),
    re_path('^api/(?P<pk>[0-9]+)/approve/$', ApproveAPIToggle.as_view(), name='api-approve'),
    re_path('^api/(?P<pk>[0-9]+)/approve-comment/$', ApproveAPIToggleComment.as_view(), name='api-approve-comment'),
    re_path('^api/(?P<pk>[0-9]+)/delete-question/$', DeleteQuestionAPIToggle.as_view(), name='api-delete-question'),
    re_path('^api/(?P<pk>[0-9]+)/delete-comment/$', DeleteCommentAPIToggle.as_view(), name='api-delete-comment'),
    re_path('^ajax/load-candidates/$', load_candidates, name='ajax-load-candidates'),
    # re_path('^api/(?P<ordering>[\w]+)/$', SortQuestionsAPI.as_view(), name='api-sort'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
