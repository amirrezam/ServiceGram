from django.db import models
from enum import Enum
from service_member.models import Institute, Gender

# Create your models here.


class ValidationStatus(Enum):
    Rej = 'Rejected'
    Pen = 'Pending'
    Act = 'Active'
    Can = 'Canceled'


class SenderStatus(Enum):
    Ins = 'Institute'
    Ben = 'Benefactor'


class WeekDay(Enum):
    Sat = 'Saturday'
    Sun = 'Sunday'
    Mon = 'Monday'
    Tue = 'Tuesday'
    Wed = 'Wednesday'
    Thu = 'Thursday'
    Fri = 'Friday'


class Requirement(models.Model):
    title = models.CharField(max_length=30, default='بی‌عنوان')
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class CashRequirement(Requirement):
    fund = models.IntegerField()
    # donated_fund = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='image/', default='image/default-img.jpg')
    owner = models.ForeignKey(
        to='service_member.Institute',
        related_name='cash_requirements',
        on_delete=models.CASCADE
    )


class NonCashRequirement(Requirement):
    beginning_date = models.DateField()
    ending_date = models.DateField()
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
    week_day = models.CharField(
        max_length=17,
        choices=[(tag, tag.value) for tag in WeekDay]
    )
    gender = models.CharField(
        max_length=5,
        default=Gender.Man
        ,   choices=[(tag, tag.value) for tag in Gender])


class Chunk(models.Model):
    beginning_time = models.TimeField()
    ending_time = models.TimeField()

    def get_beginning_time_str(self):
        if self.beginning_time.minute >= 10:
            return str(self.beginning_time.hour) + ':' + str(self.beginning_time.minute)
        else:
            return str(self.beginning_time.hour) + ':0' + str(self.beginning_time.minute)

    def get_ending_time_str(self):
        if self.ending_time.minute >= 10:
            return str(self.ending_time.hour) + ':' + str(self.ending_time.minute)
        else:
            return str(self.ending_time.hour) + ':0' + str(self.ending_time.minute)

    def __str__(self):
        return str(self.beginning_time) + ' - ' + str(self.ending_time)

    def has_conflict(self, other_chunk):
        return True


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
    date_donated = models.DateTimeField(null=True, blank=True)


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
    date_accepted = models.DateTimeField(null=True, blank=True)
