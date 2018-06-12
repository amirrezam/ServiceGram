from django import forms
from service_member.models import Skill


class CreateSkillForm(forms.ModelForm):

    class Meta:
        model = Skill
        fields = ('name',)


