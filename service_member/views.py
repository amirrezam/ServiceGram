from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, DetailView, RedirectView
from service_member.forms import SignUpInstituteForm, SignUpBenefactorForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from service_member.models import Benefactor, Institute, Member


# Create your views here.


class SignUpInstituteView(CreateView):
    form_class = SignUpInstituteForm
    success_url = '/login/'
    template_name = 'home_signup_institute.html'


class SignUpBenefactorView(CreateView):
    form_class = SignUpBenefactorForm
    success_url = '/login/'
    template_name = 'home_signup_benefactor.html'


class HomeView(TemplateView):
    template_name = 'home.html'


class ProfileView(DetailView):
    model = Member
    template_name = 'all_profile.html'

    def get_object(self, queryset=None):
        return Member.objects.get(username=self.kwargs['username'])


class ProfileRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return '/profile/' + self.request.user.username

