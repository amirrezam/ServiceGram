from django.http import Http404
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, RedirectView, ListView

from service_member.models import Skill
from service_requirement.forms import CreateCashRequirementForm, CreateNonCashRequirementForm, RequestHelpBenefactorForm
from service_requirement.models import CashRequirement, NonCashRequirement, HelpNonCash, ValidationStatus, Chunk


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
        skills = [has_skill.skill_type.name for has_skill in request.user.benefactor.skill.filter(validation_status='ValidationStatus.Act')]
        if NonCashRequirement.objects.get(pk=self.kwargs['pk']).skill.name not in skills:
            raise Http404
        if HelpNonCash.objects.filter(requirement__date__exact=NonCashRequirement.objects.get(pk=self.kwargs['pk']).date,
                                      requirement__time__exact=NonCashRequirement.objects.get(pk=self.kwargs['pk']).time,
                                      benefactor__member__username__exact=request.user.username,
                                      status='ValidationStatus.Act').count() > 0:
            raise Http404
        return super().get(request, *args, **kwargs)


class ShowRequestsRequirementView(ListView):
    model = HelpNonCash
    template_name = 'ShowRequestsRequirement.html'

    def get_queryset(self):
        return HelpNonCash.objects.filter(requirement_id__exact=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if request.user.is_benefactor or request.user.username != NonCashRequirement.objects.get(pk=self.kwargs['pk']).owner.member.username:
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
        HelpNonCash.objects.filter(requirement__time__exact=help_non_cash.requirement.time,
                                   benefactor__member__username__exact=help_non_cash.benefactor.member.username,
                                   status='ValidationStatus.Pen')\
            .update(status=ValidationStatus.Can)
        HelpNonCash.objects.filter(pk=self.kwargs['pk']).update(status=ValidationStatus.Act)
        # if HelpNonCash.objects.filter(benefactor__member__username__exact=help_non_cash.benefactor.member.username,
        #                               status='ValidationStatus.Act',
        #                               date)# TODO: how to get the number of requests in the week?
        return super().get(request, *args, **kwargs)


class ShowNonCashRequirementsView(ListView):
    template_name = 'non_cash_requirement_search.html'
    model = NonCashRequirement

    def get_queryset(self):
        ans = NonCashRequirement.objects
        if dict(self.request.GET).keys().__len__() == 0:
            return ans
        if not self.request.GET.get('day') == '':
            ans = ans.filter(date__day=self.request.GET.get('day'))
        if not self.request.GET.get('year') == '':
            ans = ans.filter(date__year=self.request.GET.get('year'))
        if not self.request.GET.get('month') == '':
            ans = ans.filter(date__month=self.request.GET.get('month'))
        if 'chunks' in dict(self.request.GET).keys():
            if not self.request.GET.get('chunks') == '':
                ans = ans.filter(time_id__in=dict(self.request.GET)['chunks'])
        if 'skills' in dict(self.request.GET).keys():
            if not self.request.GET.get('skills') == '':
                ans = ans.filter(skill_id__in=dict(self.request.GET)['skills'])
        return ans

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Skill'] = Skill.objects.all()
        context['Chunk'] = Chunk.objects.all()
        return context