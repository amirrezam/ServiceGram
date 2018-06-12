from service_admin.views import CreateSkillView
from django.contrib.auth import views as auth_views
from django.urls import re_path

urlpatterns = [
    re_path(r'$', CreateSkillView.as_view(), name='admin_home')
]
