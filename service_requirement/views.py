from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, RedirectView, ListView, FormView
from django.urls import reverse_lazy


from service_member.models import Skill, Member
from service_requirement.forms import CreateCashRequirementForm, CreateNonCashRequirementForm, \
    RequestHelpBenefactorForm, RequestHelpInstituteForm, RateHelpNonCashBenefactorForm, RateHelpNonCashInstituteForm, \
    HelpCashForm
from service_requirement.models import CashRequirement, NonCashRequirement, HelpNonCash, ValidationStatus, Chunk, WeekDay
import datetime
import jalali

# Create your views here.


class CreateCashRequirementView(CreateView):
    form_class = CreateCashRequirementForm
    template_name = 'Create.html'
    success_url = '/profile/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user.institute
        obj.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_benefactor:
            raise Http404
        if not request.user.activation_status == 'ActivationStatus.Act':
            raise Http404
        return super().get(request, *args, **kwargs)


class CreateNonCashRequirementView(CreateView):
    form_class = CreateNonCashRequirementForm
    template_name = 'Create.html'
    success_url = '/profile/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user.institute
        obj.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_benefactor:
            raise Http404
        if not request.user.activation_status == 'ActivationStatus.Act':
            raise Http404
        return super().get(request, *args, **kwargs)


class CashRequirementProfileView(DetailView):
    model = CashRequirement
    template_name = 'CashRequirementProfile.html'

    def get_object(self, queryset=None):
        return CashRequirement.objects.get(pk=self.kwargs['pk'])


class NonCashRequirementProfileView(DetailView):
    model = NonCashRequirement
    template_name = 'NonCashRequirementProfile.html'

    def get_object(self, queryset=None):
        return NonCashRequirement.objects.get(pk=self.kwargs['pk'])


class RequestHelpBenefactorView(CreateView):
    form_class = RequestHelpBenefactorForm
    template_name = 'SubmitRequest.html'
    success_url = '/profile/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.benefactor = self.request.user.benefactor
        obj.requirement = NonCashRequirement.objects.get(pk=self.kwargs['pk'])
        obj.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_institute:
            raise Http404
        skills = [has_skill.skill_type.name for has_skill in
                  request.user.benefactor.skill.filter(validation_status='ValidationStatus.Act')]

        help_non_cash = NonCashRequirement.objects.get(pk=self.kwargs['pk'])

        if help_non_cash.skill.name not in skills:
            raise Http404

        if HelpNonCash.objects.filter(requirement__time__exact=help_non_cash.requirement.time,
                                      benefactor__member__username__exact=help_non_cash.benefactor.member.username,
                                      requirement__week_day=help_non_cash.requirement.week_day,
                                      requirement__beginning_date__gte=help_non_cash.requirement.beginning_date,
                                      requirement__beginning_date__lte=help_non_cash.requirement.ending_date,
                                      status='ValidationStatus.Act').count() > 0:
            raise Http404

        if HelpNonCash.objects.filter(requirement__time__exact=help_non_cash.requirement.time,
                                      benefactor__member__username__exact=help_non_cash.benefactor.member.username,
                                      requirement__week_day=help_non_cash.requirement.week_day,
                                      requirement__ending_date__gte=help_non_cash.requirement.beginning_date,
                                      requirement__ending_date__lte=help_non_cash.requirement.ending_date,
                                      status='ValidationStatus.Act').count() > 0:
            raise Http404

        if HelpNonCash.objects.filter(requirement__time__exact=help_non_cash.requirement.time,
                                      benefactor__member__username__exact=help_non_cash.benefactor.member.username,
                                      requirement__week_day=help_non_cash.requirement.week_day,
                                      requirement__beginning_date__lte=help_non_cash.requirement.beginning_date,
                                      requirement__ending_date__gte=help_non_cash.requirement.ending_date,
                                      status='ValidationStatus.Act').count() > 0:
            raise Http404
        return super().get(request, *args, **kwargs)


class RequestHelpInstituteView(CreateView):
    form_class = RequestHelpInstituteForm
    template_name = 'SubmitRequest.html'
    success_url = '/profile/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.benefactor = Member.objects.get(username=self.kwargs['username']).benefactor
        obj.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_benefactor:
            raise Http404
        if not request.user.activation_status == 'ActivationStatus.Act':
            raise Http404
        # skills = [has_skill.skill_type.name for has_skill in
        #           request.user.benefactor.skill.filter(validation_status='ValidationStatus.Act')]
        #     if NonCashRequirement.objects.get(pk=self.kwargs['pk']).skill.name not in skills:
        #         raise Http404
        #     if HelpNonCash.objects.filter(
        #             requirement__date__exact=NonCashRequirement.objects.get(pk=self.kwargs['pk']).date,
        #             requirement__time__exact=NonCashRequirement.objects.get(pk=self.kwargs['pk']).time,
        #             benefactor__member__username__exact=request.user.username,
        #             status='ValidationStatus.Act').count() > 0:
        #         raise Http404
        return super().get(request, *args, **kwargs)


class ShowRequestsRequirementView(ListView):
    model = HelpNonCash
    template_name = 'ShowRequestsRequirement.html'

    def get_queryset(self):
        return HelpNonCash.objects.filter(requirement_id__exact=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_benefactor or request.user.username != NonCashRequirement.objects.get(
                pk=self.kwargs['pk']).owner.member.username:
            raise Http404
        if not request.user.activation_status == 'ActivationStatus.Act':
            raise Http404
        return super().get(request, *args, **kwargs)


class AcceptRequestFromBenefactorView(RedirectView):
    url = '/profile/'

    def get(self, request, *args, **kwargs):
        help_non_cash = HelpNonCash.objects.get(pk=self.kwargs['pk'])
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_benefactor:
            raise Http404
        if request.user.username != help_non_cash.requirement.owner.member.username:
            raise Http404
        if help_non_cash.status != 'ValidationStatus.Pen':
            raise Http404
        if not request.user.activation_status == 'ActivationStatus.Act':
            raise Http404
        HelpNonCash.objects.filter(requirement__time__exact=help_non_cash.requirement.time,
                                   benefactor__member__username__exact=help_non_cash.benefactor.member.username,
                                   requirement__week_day=help_non_cash.requirement.week_day,
                                   requirement__beginning_date__gte=help_non_cash.requirement.beginning_date,
                                   requirement__beginning_date__lte=help_non_cash.requirement.ending_date,
                                   status='ValidationStatus.Pen'). \
            update(status=ValidationStatus.Can)
        HelpNonCash.objects.filter(requirement__time__exact=help_non_cash.requirement.time,
                                   benefactor__member__username__exact=help_non_cash.benefactor.member.username,
                                   requirement__week_day=help_non_cash.requirement.week_day,
                                   requirement__ending_date__gte=help_non_cash.requirement.beginning_date,
                                   requirement__ending_date__lte=help_non_cash.requirement.ending_date,
                                   status='ValidationStatus.Pen'). \
            update(status=ValidationStatus.Can)
        HelpNonCash.objects.filter(requirement__time__exact=help_non_cash.requirement.time,
                                   benefactor__member__username__exact=help_non_cash.benefactor.member.username,
                                   requirement__week_day=help_non_cash.requirement.week_day,
                                   requirement__beginning_date__lte=help_non_cash.requirement.beginning_date,
                                   requirement__ending_date__gte=help_non_cash.requirement.ending_date,
                                   status='ValidationStatus.Pen'). \
            update(status=ValidationStatus.Can)
        HelpNonCash.objects.filter(pk=self.kwargs['pk']).update(status=ValidationStatus.Act)
        HelpNonCash.objects.filter(pk=self.kwargs['pk']).update(date_accepted=datetime.datetime.now())
        return super().get(request, *args, **kwargs)


class AcceptRequestFromInstituteView(RedirectView):
    url = reverse_lazy('profile_institute_requests')

    def get(self, request, *args, **kwargs):
        help_non_cash = HelpNonCash.objects.get(pk=self.kwargs['pk'])
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_institute:
            raise Http404
        if request.user.username != help_non_cash.benefactor.member.username:
            raise Http404
        if help_non_cash.status != 'ValidationStatus.Pen':
            raise Http404
        if not request.user.activation_status == 'ActivationStatus.Act':
            raise Http404
        HelpNonCash.objects.filter(requirement__time__exact=help_non_cash.requirement.time,
                                   benefactor__member__username__exact=help_non_cash.benefactor.member.username,
                                   requirement__week_day=help_non_cash.requirement.week_day,
                                   requirement__beginning_date__gte=help_non_cash.requirement.beginning_date,
                                   requirement__beginning_date__lte=help_non_cash.requirement.ending_date,
                                   status='ValidationStatus.Pen'). \
            update(status=ValidationStatus.Can)
        HelpNonCash.objects.filter(requirement__time__exact=help_non_cash.requirement.time,
                                   benefactor__member__username__exact=help_non_cash.benefactor.member.username,
                                   requirement__week_day=help_non_cash.requirement.week_day,
                                   requirement__ending_date__gte=help_non_cash.requirement.beginning_date,
                                   requirement__ending_date__lte=help_non_cash.requirement.ending_date,
                                   status='ValidationStatus.Pen'). \
            update(status=ValidationStatus.Can)
        HelpNonCash.objects.filter(requirement__time__exact=help_non_cash.requirement.time,
                                   benefactor__member__username__exact=help_non_cash.benefactor.member.username,
                                   requirement__week_day=help_non_cash.requirement.week_day,
                                   requirement__beginning_date__lte=help_non_cash.requirement.beginning_date,
                                   requirement__ending_date__gte=help_non_cash.requirement.ending_date,
                                   status='ValidationStatus.Pen'). \
            update(status=ValidationStatus.Can)
        HelpNonCash.objects.filter(pk=self.kwargs['pk']).update(status=ValidationStatus.Act)
        HelpNonCash.objects.filter(pk=self.kwargs['pk']).update(date_accepted=datetime.datetime.now())
        return super().get(request, *args, **kwargs)


class ShowNonCashRequirementsView(ListView):
    template_name = 'non_cash_requirement_search.html'
    model = NonCashRequirement

    def get_queryset(self):
        ans = NonCashRequirement.objects
        if dict(self.request.GET).keys().__len__() == 0:
            return ans

        if not (self.request.GET.get('begin_day') == '' or
                self.request.GET.get('begin_year') == '' or
                self.request.GET.get('begin_month') == ''):
            (begin_year, begin_month, begin_day) = jalali.\
                Persian((self.request.GET.get('begin_year'), self.request.GET.get('begin_month'), self.request.GET.get('begin_day'))).gregorian_tuple()
            ans = ans.filter(beginning_date__gte=
                             datetime.date(begin_year, begin_month, begin_day))

        if not (self.request.GET.get('end_day') == '' or
                self.request.GET.get('end_year') == '' or
                self.request.GET.get('end_month') == ''):
            (end_year, end_month, end_day) = jalali.\
                Persian((self.request.GET.get('end_year'), self.request.GET.get('end_month'), self.request.GET.get('end_day'))).gregorian_tuple()
            ans = ans.filter(beginning_date__gte=
                             datetime.date(end_year, end_month, end_day))


        if 'chunks' in dict(self.request.GET).keys():
            if not self.request.GET.get('chunks') == '':
                ans = ans.filter(time_id__in=dict(self.request.GET)['chunks'])
        if 'skills' in dict(self.request.GET).keys():
            if not self.request.GET.get('skills') == '':
                ans = ans.filter(skill_id__in=dict(self.request.GET)['skills'])
        if 'week_days' in dict(self.request.GET).keys():
            if not self.request.GET.get('week_days') == '':
                ans = ans.filter(week_day__in=dict(self.request.GET)['week_days'])
        return ans

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Skill'] = Skill.objects.all()
        context['Chunk'] = Chunk.objects.all()
        context['WeekDay'] = WeekDay.__members__
        return context


class RejectRequestFromBenefactorView(RedirectView):
    url = '/profile/'

    def get(self, request, *args, **kwargs):
        help_non_cash = HelpNonCash.objects.get(pk=self.kwargs['pk'])
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_benefactor:
            raise Http404
        if request.user.username != help_non_cash.requirement.owner.member.username:
            raise Http404
        if help_non_cash.status != 'ValidationStatus.Pen':
            raise Http404
        if not request.user.activation_status == 'ActivationStatus.Act':
            raise Http404
        HelpNonCash.objects.filter(pk=self.kwargs['pk']).update(status=ValidationStatus.Rej)
        HelpNonCash.objects.filter(pk=self.kwargs['pk']).update(date_accepted=datetime.datetime.now())
        return super().get(request, *args, **kwargs)


class RejectRequestFromInstituteView(RedirectView):
    url = '/profile/'

    def get(self, request, *args, **kwargs):
        help_non_cash = HelpNonCash.objects.get(pk=self.kwargs['pk'])
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_institute:
            raise Http404
        if request.user.username != help_non_cash.benefactor.member.username:
            raise Http404
        if help_non_cash.status != 'ValidationStatus.Pen':
            raise Http404
        if not request.user.activation_status == 'ActivationStatus.Act':
            raise Http404
        HelpNonCash.objects.filter(pk=self.kwargs['pk']).update(status=ValidationStatus.Rej)
        HelpNonCash.objects.filter(pk=self.kwargs['pk']).update(date_accepted=datetime.datetime.now())
        return super().get(request, *args, **kwargs)


class RateHelpNonCashBenefactorView(FormView):
    form_class = RateHelpNonCashBenefactorForm
    template_name = 'SubmitRequest.html'
    success_url = '/profile/'

    def form_valid(self, form):
        HelpNonCash.objects.filter(requirement_id__exact=self.kwargs['pk'],
                                   benefactor__member__username__exact=self.request.user.username). \
            update(institute_score=form.cleaned_data['rate'])
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        help_non_cash = get_object_or_404(HelpNonCash, requirement_id__exact=self.kwargs['pk'],
                                          benefactor__member__username__exact=self.request.user.username)
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_institute:
            raise Http404
        if request.user.username != help_non_cash.benefactor.member.username:
            raise Http404
        if help_non_cash.status != 'ValidationStatus.Act':
            raise Http404
        if not request.user.activation_status == 'ActivationStatus.Act':
            raise Http404
        return super().get(request, *args, **kwargs)


class RateHelpNonCashInstituteView(FormView):
    form_class = RateHelpNonCashInstituteForm
    template_name = 'SubmitRequest.html'
    success_url = '/profile/'

    def form_valid(self, form):
        HelpNonCash.objects.filter(requirement_id__exact=self.kwargs['pk'],
                                   benefactor__member__username__exact=self.kwargs['username']). \
            update(benefactor_score=form.cleaned_data['rate'])
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        help_non_cash = get_object_or_404(HelpNonCash, requirement_id__exact=self.kwargs['pk'],
                                          benefactor__member__username__exact=self.kwargs['username'])
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_benefactor:
            raise Http404
        if request.user.username != help_non_cash.requirement.owner.member.username:
            raise Http404
        if help_non_cash.status != 'ValidationStatus.Act':
            raise Http404
        if not request.user.activation_status == 'ActivationStatus.Act':
            raise Http404
        return super().get(request, *args, **kwargs)


class HelpCashView(FormView):
    form_class = HelpCashForm
    template_name = 'SubmitRequest.html'
    success_url = '/profile/'

    def form_valid(self, form):
        form.save(commit=True)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['requirement'] = CashRequirement.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if not request.user.is_benefactor:
            raise Http404
        if not request.user.activation_status == 'ActivationStatus.Act':
            raise Http404
        return super().get(request, *args, **kwargs)
