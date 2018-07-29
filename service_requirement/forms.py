import datetime
from django import forms
from django.core.exceptions import ValidationError

from service_requirement.models import CashRequirement, NonCashRequirement, Chunk, HelpNonCash, ValidationStatus, \
    SenderStatus, WeekDay, HelpCash
from service_member.models import Skill, Member
import jalali


class CreateCashRequirementForm(forms.ModelForm):
    def save(self, commit=True):
        cash_requirement = super().save(commit=False)
        # cash_requirement.donated_fund = 0
        return cash_requirement

    class Meta:
        model = CashRequirement
        fields = ('fund', 'description', 'title', 'avatar')


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
    week_day = forms.ChoiceField(
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['week_day'].choices = [(tag, tag.value) for tag in WeekDay]

    def save(self, commit=True):
        non_cash_requirement = super().save(commit=False)
        non_cash_requirement.time = self.cleaned_data.get('time')
        non_cash_requirement.skill = self.cleaned_data.get('skill')
        non_cash_requirement.week_day = self.cleaned_data.get('week_day')
        return non_cash_requirement

    class Meta:
        model = NonCashRequirement
        fields = ('description', 'title')


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


class HelpCashForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.requirement = kwargs.pop('requirement', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        help_cash = super().save(commit=False)
        help_cash.benefactor = self.user.benefactor
        help_cash.requirement = self.requirement
        help_cash.date_donated = datetime.datetime.now()
        if commit:
            help_cash.save()
        return help_cash

    class Meta:
        model = HelpCash
        fields = ('amount',)


class RequestHelpInstituteForm(forms.ModelForm):
    requirement = forms.ChoiceField(
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['requirement'].choices = [(requirement.pk, requirement.title) for requirement in self.user.institute.non_cash_requirements.all()]

    def save(self, commit=True):
        help_non_cash = super().save(commit=False)
        help_non_cash.status = ValidationStatus.Pen
        help_non_cash.sender = SenderStatus.Ins
        help_non_cash.benefactor_score = -1
        help_non_cash.institute_score = -1
        help_non_cash.requirement = NonCashRequirement.objects.get(pk=self.cleaned_data.get('requirement'))
        return help_non_cash

    class Meta:
        model = HelpNonCash
        fields = ('description',)


class RateHelpNonCashBenefactorForm(forms.Form):
    rate = forms.IntegerField()


class RateHelpNonCashInstituteForm(forms.Form):
    rate = forms.IntegerField()

