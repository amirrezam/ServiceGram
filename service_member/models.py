from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum

# Create your models here.


class ActivationStatus(Enum):
    Rej = 'Rejected'
    Pen = 'Pending'
    Act = 'Active'


class Member(AbstractUser):
    activation_status = models.CharField(
        max_length=8,
        choices=[(tag, tag.value) for tag in ActivationStatus]
    )
    is_benefactor = models.BooleanField(default=True)
    is_institute = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'Member'


class Institute(models.Model):
    member = models.OneToOneField(to='Member', related_name='institute', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Institute'


class Benefactor(models.Model):
    member = models.OneToOneField(to='Member', related_name='benefactor', on_delete=models.CASCADE, null=True)
    max_chunk_in_week = models.IntegerField(default=20)
    skill = models.ManyToManyField(to='Skill', related_name='benefactors', blank=True, default=None)

    class Meta:
        verbose_name = 'Benefactor'


class Skill(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
