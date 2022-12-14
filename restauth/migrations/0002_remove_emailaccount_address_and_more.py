# Generated by Django 4.0.6 on 2022-09-09 22:51

import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('restauth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailaccount',
            name='address',
        ),
        migrations.RemoveField(
            model_name='emailaccount',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='emailaccount',
            name='full_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='emailaccount',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='emailaccount',
            name='username',
            field=models.CharField(default=0, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
            preserve_default=False,
        ),
    ]
