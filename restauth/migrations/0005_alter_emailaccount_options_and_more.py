# Generated by Django 4.0.6 on 2022-09-15 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restauth', '0004_alter_emailaccount_full_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailaccount',
            options={},
        ),
        migrations.RemoveField(
            model_name='emailaccount',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='emailaccount',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='emailaccount',
            name='last_name',
        ),
    ]
