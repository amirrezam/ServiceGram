from django.shortcuts import render
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from service_admin.forms import CreateSkillForm

# Create your views here.


class CreateSkillView(CreateView):
    form_class = CreateSkillForm
    template_name = 'base.html'
    success_url = reverse_lazy('admin_home')

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if not request.user.is_superuser:
            raise Http404
        return super().get(request, *args, **kwargs)
