# Generated by Django 2.0.5 on 2018-07-26 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_member', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='institute',
            name='lat',
            field=models.DecimalField(decimal_places=10, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='institute',
            name='long',
            field=models.DecimalField(decimal_places=10, max_digits=20, null=True),
        ),
    ]
