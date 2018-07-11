from django.shortcuts import render
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, RedirectView
from service_admin.forms import CreateSkillForm, CreateChunkForm
from service_member.models import Skill, HasSkill, Member


# Create your views here.
from service_requirement.models import Chunk


class CreateSkillView(CreateView):
    form_class = CreateSkillForm
    template_name = 'create_skill.html'
    success_url = reverse_lazy('add_skill')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Skills'] = Skill.objects
        context['HasSkills'] = HasSkill.objects
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


class RejectSkillView(RedirectView):
    url = reverse_lazy('validate_skill')

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if not request.user.is_superuser:
            raise Http404
        HasSkill.objects.filter(pk=self.kwargs['pk']).update(validation_status='ValidationStatus.Rej')
        return super().get(request, *args, **kwargs)


class ValidateUserView(ListView):
    model = Member
    template_name = 'validate_user.html'

    def get_queryset(self):
        return Member.objects.filter(activation_status="ActivationStatus.Pen")

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if not request.user.is_superuser:
            raise Http404
        return super().get(request, *args, **kwargs)


class AcceptUserView(RedirectView):
    url = reverse_lazy('validate_user')

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if not request.user.is_superuser:
            raise Http404
        Member.objects.filter(pk=self.kwargs['pk']).update(activation_status="ActivationStatus.Act")
        return super().get(request, *args, **kwargs)


class RejectUserView(RedirectView):
    url = reverse_lazy('validate_user')

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if not request.user.is_superuser:
            raise Http404
        Member.objects.filter(pk=self.kwargs['pk']).update(activation_status="ActivationStatus.Rej")
        return super().get(request, *args, **kwargs)


class CreateChunkView(CreateView):
    form_class = CreateChunkForm
    template_name = 'create_chunk.html'
    success_url = reverse_lazy('add_chunk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Chunks'] = Chunk.objects
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if not request.user.is_superuser:
            raise Http404
        return super().get(request, *args, **kwargs)
