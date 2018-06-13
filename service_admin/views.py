from django.shortcuts import render
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, RedirectView
from service_admin.forms import CreateSkillForm
from service_member.models import Skill, HasSkill

# Create your views here.


class CreateSkillView(CreateView):
    form_class = CreateSkillForm
    template_name = 'create_skill.html'
    success_url = reverse_lazy('add_skill')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Skills'] = Skill.objects
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if not request.user.is_superuser:
            raise Http404
        return super().get(request, *args, **kwargs)


class ValidateSkillView(ListView):
    model = HasSkill
    template_name = 'validate_skill.html'

    def get_queryset(self):
        return HasSkill.objects.filter(validation_status='ValidationStatus.Pen')

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if not request.user.is_superuser:
            raise Http404
        return super().get(request, *args, **kwargs)


class AcceptSkillView(RedirectView):
    url = reverse_lazy('validate_skill')

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if not request.user.is_superuser:
            raise Http404
        HasSkill.objects.filter(pk=self.kwargs['pk']).update(validation_status='ValidationStatus.Act')
        return super().get(request, *args, **kwargs)

