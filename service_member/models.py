from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum

# Create your models here.


class ActivationStatus(Enum):
    Rej = 'Rejected'
    Pen = 'Pending'
    Act = 'Active'


class Gender(Enum):
    Man = 'Man'
    Woman = 'Woman'


class Member(AbstractUser):
    activation_status = models.CharField(
        max_length=8,
        choices=[(tag, tag.value) for tag in ActivationStatus]
    )
    is_benefactor = models.BooleanField(default=True)
    is_institute = models.BooleanField(default=False)
    bio = models.CharField(max_length=200, null=True, blank=True)
    avatar = models.ImageField(upload_to='image/', default='image/default-img.png')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Member'


class Institute(models.Model):
    member = models.OneToOneField(to='Member', related_name='institute', on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    lat = models.DecimalField(null=True, max_digits=20, decimal_places=10)
    long = models.DecimalField(null=True, max_digits=20, decimal_places=10)
    telephone_number = models.CharField(null=True, max_length=17)

    class Meta:
        verbose_name = 'Institute'

    def __str__(self):
        return self.member.username


class Photo(models.Model):
    image = models.ImageField(upload_to='image/')
    institute = models.ForeignKey('Institute', on_delete=models.CASCADE, related_name="images")


class Benefactor(models.Model):
    member = models.OneToOneField(to='Member', related_name='benefactor', on_delete=models.CASCADE, null=True)

    gender = models.CharField(
        max_length=5,
        default=Gender.Man
        ,   choices=[(tag, tag.value) for tag in Gender])

    class Meta:
        verbose_name = 'Benefactor'

    def __str__(self):
        return self.member.username


class Skill(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class HasSkill(models.Model):
    skill_type = models.ForeignKey(
        to='Skill',
        related_name='benefactors',
        blank=True,
        default=None,
        on_delete=models.CASCADE
    )
    benefactor = models.ForeignKey(
        to='Benefactor',
        related_name='skill',
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE
    )
    validation_status = models.CharField(
        max_length=8,
        choices=[(tag, tag.value) for tag in ActivationStatus]
    )

    def __str__(self):
        return str(self.skill_type)
