from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import QuerySet

from service_member.models import Member, Institute, Benefactor, Skill, HasSkill
from service_requirement.models import ValidationStatus


class SignUpInstituteForm(UserCreationForm):
    def save(self, commit=True):
        member = super().save(commit=False)
        member.is_benefactor = False
        member.is_institute = True
        member.save()
        institute = Institute.objects.create(member=member)
        return member

    class Meta:
        model = Member
        fields = ('username', 'first_name', 'email', 'password1', 'password2', 'bio')


class SignUpBenefactorForm(UserCreationForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def save(self, commit=True):
        member = super().save(commit=False)
        member.is_benefactor = True
        member.is_institute = False
        member.save()
        benefactor = Benefactor.objects.create(member=member)
        print(self.cleaned_data.get('skills').all())
        for skill in self.cleaned_data.get('skills').all():
            has_skill = HasSkill.objects.create(benefactor=benefactor, skill_type=skill,
                                                validation_status=ValidationStatus.Pen)
            has_skill.save()
            benefactor.skill.add(has_skill)
        benefactor.save()
        return member

    class Meta:
        model = Member
        fields = ('username', 'first_name', 'last_name', 'email', 'bio', 'password1', 'password2')
