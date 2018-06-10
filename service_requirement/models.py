from django.db import models
from enum import Enum
from service_member.models import Institute

# Create your models here.


class ValidationStatus(Enum):
    Rej = 'Rejected'
    Pen = 'Pending'
    Act = 'Active'
    Can = 'Canceled'


class SenderStatus(Enum):
    Ins = 'Institute'
    Ben = 'Benefactor'


class Requirement(models.Model):
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class CashRequirement(Requirement):
    fund = models.IntegerField()
    donated_fund = models.IntegerField(default=0)
    owner = models.ForeignKey(
        to='service_member.Institute',
        related_name='cash_requirements',
        on_delete=models.CASCADE
    )


class NonCashRequirement(Requirement):
    date = models.DateField()
    time = models.ForeignKey(
        to='Chunk',
        related_name='requirements',
        null=True,
        on_delete=models.SET_NULL
    )
    owner = models.ForeignKey(
        to='service_member.Institute',
        related_name='non_cash_requirements',
        on_delete=models.CASCADE
    )
    skill = models.ForeignKey(
        to='service_member.Skill',
        related_name='non_cash_requirements',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


class Chunk(models.Model):
    beginning_time = models.TimeField()
    ending_time = models.TimeField()

    def __str__(self):
        return str(self.beginning_time) + ' - ' + str(self.ending_time)


class HelpCash(models.Model):
    amount = models.IntegerField()
    benefactor = models.ForeignKey(
        to='service_member.Benefactor',
        related_name='cash_helps',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    requirement = models.ForeignKey(
        to='CashRequirement',
        related_name='helps',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )


class HelpNonCash(models.Model):
    description = models.CharField(max_length=100)
    status = models.CharField(
        max_length=8,
        choices=[(tag, tag.value) for tag in ValidationStatus]
    )
    sender = models.CharField(
        max_length=10,
        choices=[(tag, tag.value) for tag in SenderStatus]
    )
    benefactor_score = models.IntegerField()
    institute_score = models.IntegerField()
    benefactor = models.ForeignKey(
        to='service_member.Benefactor',
        related_name='non_cash_helps',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    requirement = models.ForeignKey(
        to='NonCashRequirement',
        related_name='helps',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
