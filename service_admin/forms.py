from django import forms
from service_member.models import Skill
from service_requirement.models import Chunk


class CreateSkillForm(forms.ModelForm):

    class Meta:
        model = Skill
        fields = ('name',)


class CreateChunkForm(forms.ModelForm):

    class Meta:
        model = Chunk
        fields = ('beginning_time', 'ending_time')


