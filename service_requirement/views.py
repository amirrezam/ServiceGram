from django.http import Http404
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, RedirectView, ListView
from service_requirement.forms import CreateCashRequirementForm, CreateNonCashRequirementForm, RequestHelpBenefactorForm
from service_requirement.models import CashRequirement, NonCashRequirement, HelpNonCash, ValidationStatus


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
    success_url = '/login/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.benefactor = self.request.user.benefactor
        obj.requirement = NonCashRequirement.objects.get(pk=self.kwargs['pk'])
        obj.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_institute:
            raise Http404
        return super().get(request, *args, **kwargs)


class ShowRequestsRequirementView(ListView):
    model = HelpNonCash
    template_name = 'ShowRequestsRequirement.html'

    def get_queryset(self):
        return HelpNonCash.objects.filter(requirement_id__exact=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        if request.user.is_benefactor or request.user.username != NonCashRequirement.objects.get(pk=self.kwargs['pk']).owner.member.username:
            raise Http404
        return super().get(request, *args, **kwargs)


class AcceptRequestFromBenefactorView(RedirectView):
    url = '/profile/'

    def get(self, request, *args, **kwargs):
        help_non_cash = HelpNonCash.objects.get(pk=self.kwargs['pk'])
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
