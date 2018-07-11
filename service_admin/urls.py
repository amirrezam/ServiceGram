from service_admin.views import CreateSkillView, ValidateSkillView, AcceptSkillView, RejectSkillView, ValidateUserView, \
    AcceptUserView, RejectUserView, CreateChunkView
from django.contrib.auth import views as auth_views
from django.urls import re_path

urlpatterns = [
    re_path(r'skills/new/$', CreateSkillView.as_view(), name='add_skill'),
    re_path(r'skills/validate/$', ValidateSkillView.as_view(), name='validate_skill'),
    re_path(r'skills/accept/(?P<pk>[a-zA-Z0-9]+)/$', AcceptSkillView.as_view(), name='accept_skill'),
    re_path(r'skills/reject/(?P<pk>[a-zA-Z0-9]+)/$', RejectSkillView.as_view(), name='reject_skill'),
    re_path(r'users/validate/$', ValidateUserView.as_view(), name='validate_user'),
    re_path(r'users/accept/(?P<pk>[a-zA-Z0-9]+)/$', AcceptUserView.as_view(), name='accept_user'),
    re_path(r'users/reject/(?P<pk>[a-zA-Z0-9]+)/$', RejectUserView.as_view(), name='reject_user'),
    re_path(r'chunks/new/$', CreateChunkView.as_view(), name='add_chunk')
]
