# Generated by Django 2.0.5 on 2018-07-19 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_requirement', '0002_helpnoncash_date_accepted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cashrequirement',
            name='donated_fund',
        ),
        migrations.AddField(
            model_name='helpcash',
            name='date_donated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
