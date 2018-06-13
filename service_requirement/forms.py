from django import forms
from django.core.exceptions import ValidationError

from service_requirement.models import CashRequirement, NonCashRequirement, Chunk, HelpNonCash, ValidationStatus, \
    SenderStatus
from service_member.models import Skill


class CreateCashRequirementForm(forms.ModelForm):
    def save(self, commit=True):
        cash_requirement = super().save(commit=False)
        cash_requirement.donated_fund = 0
        return cash_requirement

    class Meta:
        model = CashRequirement
        fields = ('fund', 'description')


class CreateNonCashRequirementForm(forms.ModelForm):
    skill = forms.ModelChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.RadioSelect,
        required=True
    )
    time = forms.ModelChoiceField(
        queryset=Chunk.objects.all(),
        widget=forms.RadioSelect,
        required=True
    )

    def save(self, commit=True):
        non_cash_requirement = super().save(commit=False)
        non_cash_requirement.time = self.cleaned_data.get('time')
        non_cash_requirement.skill = self.cleaned_data.get('skill')
        return non_cash_requirement

    class Meta:
        model = NonCashRequirement
        fields = ('date', 'description')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class RequestHelpBenefactorForm(forms.ModelForm):

    def save(self, commit=True):
        help_non_cash = super().save(commit=False)
        help_non_cash.status = ValidationStatus.Pen
        help_non_cash.sender = SenderStatus.Ben
        help_non_cash.benefactor_score = -1
        help_non_cash.institute_score = -1
        return help_non_cash

    class Meta:
        model = HelpNonCash
        fields = ('description',)

