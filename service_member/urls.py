from service_member.views import SignUpBenefactorView, SignUpInstituteView, home_view
from django.contrib.auth import views as auth_views
from django.urls import re_path

urlpatterns = [
    re_path(r'signup/benefactor/$', SignUpBenefactorView.as_view(), name='signup_benefactor'),
    re_path(r'signup/institute/$', SignUpInstituteView.as_view(), name='signup_institute'),
    re_path(r'login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    re_path(r'logout/$', auth_views.logout, name='logout'),
    re_path(r'$', home_view, name='home')
]
