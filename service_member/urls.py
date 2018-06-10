from service_member.views import SignUpBenefactorView, SignUpInstituteView, HomeView, ProfileView, ProfileRedirectView, \
    ShowInstitutesView
from django.contrib.auth import views as auth_views
from django.urls import re_path

urlpatterns = [
    re_path(r'signup/benefactor/$', SignUpBenefactorView.as_view(), name='signup_benefactor'),
    re_path(r'signup/institute/$', SignUpInstituteView.as_view(), name='signup_institute'),
    re_path(r'login/$', auth_views.login, {'template_name': 'home_login.html'}, name='login'),
    re_path(r'logout/$', auth_views.logout, name='logout'),
    re_path(r'profile/(?P<username>[a-zA-Z0-9_]+)$', ProfileView.as_view(), name='profile'),
    re_path(r'profile/$', ProfileRedirectView.as_view(), name='profile_redirect'),
    re_path(r'institutes/$', ShowInstitutesView.as_view(), name='show_non_cash_requirements'),
    re_path(r'$', HomeView.as_view(), name='home')
]
