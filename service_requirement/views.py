from django.http import Http404
from django.shortcuts import render
from django.views.generic import CreateView
from service_requirement.forms import CreateCashRequirementForm, CreateNonCashRequirementForm

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
