from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import QuerySet

from service_member.models import Member, Institute, Benefactor, Skill, HasSkill, ActivationStatus
from service_requirement.models import ValidationStatus


class SignUpInstituteForm(UserCreationForm):
    def save(self, commit=True):
        member = super().save(commit=False)
        member.is_benefactor = False
        member.is_institute = True
        member.activation_status = ActivationStatus.Pen
        member.save()
        institute = Institute.objects.create(member=member)
        return member

    class Meta:
        model = Member
        fields = ('username', 'first_name', 'email', 'password1', 'password2', 'bio', 'avatar')


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
        member.activation_status = ActivationStatus.Pen
        member.save()
        benefactor = Benefactor.objects.create(member=member)
        for skill in self.cleaned_data.get('skills').all():
            has_skill = HasSkill.objects.create(benefactor=benefactor, skill_type=skill,
                                                validation_status=ValidationStatus.Pen)
            has_skill.save()
            benefactor.skill.add(has_skill)
        benefactor.save()
        return member

    class Meta:
        model = Member
        fields = ('username', 'first_name', 'last_name', 'email', 'bio', 'password1', 'password2', 'avatar')


class EditProfileBenefactorForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['bio'].initial = self.user.bio
        self.fields['email'].initial = self.user.email
        self.fields['avatar'].initial = self.user.avatar

    class Meta:
        model = Member
        fields = ('avatar', 'email', 'bio', 'first_name', 'last_name')


class EditProfileInstituteForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ('avatar', 'email', 'bio', 'first_name')
