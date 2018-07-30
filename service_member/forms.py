from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import QuerySet

from service_member.models import Member, Institute, Benefactor, Skill, HasSkill, ActivationStatus, Photo
from service_requirement.models import ValidationStatus


class AddImageInstituteForm(forms.ModelForm):
    def save(self, commit=True):
        print(self.cleaned_data.keys(), "inja keys")
        photo = super().save(commit=False)
        return photo

    class Meta:
        model = Photo
        fields = ('image',)


class SignUpInstituteForm(UserCreationForm):
    city = forms.CharField()
    address = forms.Textarea()
    photo = forms.ImageField()

    def save(self, commit=True):
        member = super().save(commit=False)
        member.is_benefactor = False
        member.is_institute = True
        member.activation_status = ActivationStatus.Pen
        member.save()
        institute = Institute.objects.create(member=member)
        if 'city' in list(self.cleaned_data.keys()):
            institute.city = self.cleaned_data['city']
        if 'address' in list(self.cleaned_data.keys()):
            institute.address = self.cleaned_data['address']
        institute.save()
        if 'photo' in list(self.cleaned_data.keys()):
            photo = Photo.objects.create(image=self.cleaned_data['photo'], institute=institute)
        photo.save()
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
    city = forms.CharField()
    address = forms.CharField()
    lat = forms.DecimalField(required=False)
    long = forms.DecimalField(required=False)

    class Meta:
        model = Member
        fields = ('avatar', 'email', 'bio', 'first_name')
