from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, DetailView, RedirectView, ListView, FormView
from service_member.forms import SignUpInstituteForm, SignUpBenefactorForm, EditProfileBenefactorForm, \
    EditProfileInstituteForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from service_member.models import Benefactor, Institute, Member, Skill, HasSkill
from service_requirement.models import NonCashRequirement, ValidationStatus


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


class EditProfileBenefactorView(FormView):
    template_name = 'edit_profile_benefactor.html'
    form_class = EditProfileBenefactorForm
    success_url = '/profile/'

    def form_valid(self, form):
        self.request.user.avatar = form.cleaned_data['avatar']
        self.request.user.first_name = form.cleaned_data['first_name']
        self.request.user.last_name = form.cleaned_data['last_name']
        self.request.user.bio = form.cleaned_data['bio']
        self.request.user.email = form.cleaned_data['email']
        self.request.user.save()
        benefactor = self.request.user.benefactor
        for skill in form.cleaned_data.get('skills').all():
            has_skill = HasSkill.objects.create(benefactor=benefactor, skill_type=skill,
                                                validation_status=ValidationStatus.Pen)
            has_skill.save()
            benefactor.skill.add(has_skill)
        benefactor.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Skill'] = Skill.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if not request.user.is_benefactor:
            raise Http404
        return super().get(request, *args, **kwargs)


class EditProfileInstituteView(FormView):
    template_name = 'edit_profile_institute.html'
    form_class = EditProfileInstituteForm
    success_url = '/profile/'

    def form_valid(self, form):
        self.request.user.avatar = form.cleaned_data['avatar']
        self.request.user.first_name = form.cleaned_data['first_name']
        self.request.user.bio = form.cleaned_data['bio']
        self.request.user.email = form.cleaned_data['email']
        self.request.user.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if not request.user.is_institute:
            raise Http404
        return super().get(request, *args, **kwargs)


class EditProfileView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_benefactor:
            return '/edit/profile/benefactor/'
        else:
            return '/edit/profile/institute/'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        return super().get(request, *args, **kwargs)


