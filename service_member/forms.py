from django import forms
from django.contrib.auth.forms import UserCreationForm

from service_member.models import Member, Institute, Benefactor


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
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class SignUpBenefactorForm(UserCreationForm):
    def save(self, commit=True):
        member = super().save(commit=False)
        member.is_benefactor = True
        member.is_institute = False
        member.save()
        benefator = Benefactor.objects.create(member=member)
        return member

    class Meta:
        model = Member
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


# class LogInForm