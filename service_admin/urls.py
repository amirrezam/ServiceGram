from service_admin.views import CreateSkillView, ValidateSkillView, AcceptSkillView
from django.contrib.auth import views as auth_views
from django.urls import re_path

urlpatterns = [
    re_path(r'skills/new/$', CreateSkillView.as_view(), name='add_skill'),
    re_path(r'skills/validate/$', ValidateSkillView.as_view(), name='validate_skill'),
    re_path(r'skills/accept/(?P<pk>[a-zA-Z0-9]+)/$', AcceptSkillView.as_view(), name='accept_skill')
]
