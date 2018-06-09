# Generated by Django 2.0.5 on 2018-05-25 21:33

from django.db import migrations, models
import django.db.models.deletion
import service_requirement.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('service_member', '0003_auto_20180526_0156'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('fund', models.IntegerField()),
                ('donated_fund', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_requirements', to='service_member.Institute')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Chunk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beginning_time', models.IntegerField()),
                ('ending_time', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='HelpCash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('benefactor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cash_helps', to='service_member.Benefactor')),
                ('requirement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='helps', to='service_requirement.CashRequirement')),
            ],
        ),
        migrations.CreateModel(
            name='NonCashRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('date', models.DateField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='non_cash_requirements', to='service_member.Institute')),
                ('time', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requirements', to='service_requirement.Chunk')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NonHelpCash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[(service_requirement.models.ValidationStatus('Rejected'), 'Rejected'), (service_requirement.models.ValidationStatus('Pending'), 'Pending'), (service_requirement.models.ValidationStatus('Active'), 'Active'), (service_requirement.models.ValidationStatus('Canceled'), 'Canceled')], max_length=8)),
                ('sender', models.CharField(choices=[(service_requirement.models.SenderStatus('Institute'), 'Institute'), (service_requirement.models.SenderStatus('Benefactor'), 'Benefactor')], max_length=10)),
                ('benefactor_score', models.IntegerField()),
                ('institute_score', models.IntegerField()),
                ('benefactor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='non_cash_helps', to='service_member.Benefactor')),
                ('requirement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='helps', to='service_requirement.NonCashRequirement')),
            ],
        ),
    ]