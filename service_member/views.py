from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, DetailView, RedirectView, ListView, FormView
from service_member.forms import SignUpInstituteForm, SignUpBenefactorForm, EditProfileBenefactorForm, \
    EditProfileInstituteForm, AddImageInstituteForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from service_member.models import Benefactor, Institute, Member, Skill, HasSkill, Photo, Gender
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
        context['Gender'] = Gender.__members__
        return context


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Count_member'] = Member.objects.filter(is_superuser=False).count()
        context['Count_benefactor'] = Benefactor.objects.count()
        context['Count_institute'] = Institute.objects.count()
        return context


class ProfileView(DetailView):
    model = Member
    template_name = 'all_profile.html'

    def get_object(self, queryset=None):
        return Member.objects.get(username=self.kwargs['username'])


class AddImageInstituteView(FormView):
    template_name = 'SubmitRequest.html'
    form_class = AddImageInstituteForm
    success_url = '/profile/'

    def form_valid(self, form):
        print("inja salam", self.request.user.institute)
        photo = form.save(commit=False)
        photo.institute = self.request.user.institute
        photo.save()
        return super().form_valid(form)


class ProfileActivitiesView(DetailView):
    model = Member
    template_name = 'benefactor_profile_activities.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_institute:
            raise Http404
        return super().get(request, *args, **kwargs)


class ProfileOwnRequestsView(DetailView):
    model = Member
    template_name = 'benefactor_profile_own_requests.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_institute:
            raise Http404
        return super().get(request, *args, **kwargs)


class ProfileInstituteRequestsView(DetailView):
    model = Member
    template_name = 'benefactor_profile_institute_requests.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_institute:
            raise Http404
        return super().get(request, *args, **kwargs)


class ProfileArchiveView(DetailView):
    model = Member
    template_name = 'benefactor_profile_archive.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_institute:
            raise Http404
        return super().get(request, *args, **kwargs)


class ProfileCashRequirementView(DetailView):
    model = Member
    template_name = 'institute_profile_cash_requirement.html'

    def get_object(self, queryset=None):
        return Member.objects.get(username=self.kwargs['username'])

    def get(self, request, *args, **kwargs):
        if not Member.objects.get(username=self.kwargs['username']).is_institute:
            raise Http404
        return super().get(request, *args, **kwargs)


class ProfileNonCashRequirementView(DetailView):
    model = Member
    template_name = 'institute_profile_noncash_requirement.html'

    def get_object(self, queryset=None):
        return Member.objects.get(username=self.kwargs['username'])

    def get(self, request, *args, **kwargs):
        if not Member.objects.get(username=self.kwargs['username']).is_institute:
            raise Http404
        return super().get(request, *args, **kwargs)


class ProfileRatingView(DetailView):
    model = Member

    def get_object(self, queryset=None):
        return self.request.user

    def get_template_names(self):
        if self.request.user.is_benefactor:
            return 'benefactor_profile_rating.html'
        else:
            return 'institute_profile_rating.html'


class ProfileRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return '/admin1/skills/validate/'
        return '/profile/' + self.request.user.username


class ShowInstitutesView(ListView):
    template_name = 'institute_search.html'
    model = Institute

    def get_queryset(self):
        institutes = Institute.objects.filter(member__activation_status='ActivationStatus.Act')
        if 'name' in dict(self.request.GET).keys():
            return institutes.filter(member__first_name__icontains=self.request.GET.get('name'))
        else:
            return institutes


class ShowBenefactorsView(ListView):
    template_name = 'benefactor_search.html'
    model = Benefactor

    def get_queryset(self):
        benefactors = Benefactor.objects.filter(member__activation_status='ActivationStatus.Act')
        if 'name' in dict(self.request.GET).keys():
            return benefactors.filter(member__last_name__icontains=self.request.GET.get('name'))

        else:
            return benefactors


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
            flag = False
            for has_skill in benefactor.skill.all():
                if has_skill.skill_type.name == skill.name:
                    flag = True
            if flag:
                continue
            has_skill = HasSkill.objects.create(benefactor=benefactor, skill_type=skill,
                                                validation_status=ValidationStatus.Pen)
            has_skill.save()
            benefactor.skill.add(has_skill)
        for has_skill in benefactor.skill.all():
            flag = False
            for skill in form.cleaned_data.get('skills').all():
                if has_skill.skill_type.name == skill.name:
                    flag = True
            if flag:
                continue
            has_skill.delete()
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
        self.request.user.institute.lat = form.cleaned_data['lat']
        self.request.user.institute.long = form.cleaned_data['long']
        self.request.user.institute.telephone_number = form.cleaned_data['telephone_number']
        if 'city' in list(form.cleaned_data.keys()):
            self.request.user.institute.city = form.cleaned_data['city']
        if 'address' in list(form.cleaned_data.keys()):
            self.request.user.institute.address = form.cleaned_data['address']
        self.request.user.institute.save()
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
        if request.user.is_superuser:
            raise Http404
        return super().get(request, *args, **kwargs)


class VezTestView(TemplateView):
    template_name = 'test.html'

class VezTestView2(TemplateView):
    template_name = 'benefactor_profile_own_requests.html'

class VezTestView3(TemplateView):
    template_name = 'benefactor_profile_institute_requests.html'

class VezTestView4(TemplateView):
    template_name = 'benefactor_profile_archive.html'

class VezTestView5(TemplateView):
    template_name = 'benefactor_profile_rating.html'

class VezTestView6(TemplateView):
    template_name = 'institute_profile_cash_requirement.html'

class VezTestView7(TemplateView):
    template_name = 'institute_profile_noncash_requirement.html'