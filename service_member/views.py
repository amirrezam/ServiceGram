from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, DetailView, RedirectView, ListView
from service_member.forms import SignUpInstituteForm, SignUpBenefactorForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from service_member.models import Benefactor, Institute, Member, Skill
from service_requirement.models import NonCashRequirement


# Create your views here.
from service_requirement.models import Chunk


class SignUpInstituteView(CreateView):
    form_class = SignUpInstituteForm
    success_url = '/login/'
    template_name = 'home_signup_institute.html'


class SignUpBenefactorView(CreateView):
    form_class = SignUpBenefactorForm
    success_url = '/login/'
    template_name = 'home_signup_benefactor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Skill'] = Skill.objects.all()
        return context


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


class ShowInstitutesView(ListView):
    template_name = 'institute_search.html'
    model = Institute

    def get_queryset(self):
        print(self.request.GET)
        if 'name' in dict(self.request.GET).keys():
            return Institute.objects.filter(member__first_name__icontains=self.request.GET.get('name'))
        else:
            return Institute.objects


class ShowBenefactorsView(ListView):
    template_name = 'benefactor_search.html'
    model = Benefactor

    def get_queryset(self):
        print(self.request.GET)
        if 'name' in dict(self.request.GET).keys():
            return Benefactor.objects.filter(member__first_name__icontains=self.request.GET.get('name'))
        else:
            return Benefactor.objects

