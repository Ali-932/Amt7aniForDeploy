# Generated by Django 4.0.6 on 2022-09-15 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0023_alter_quiz_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='quiz',
            unique_together={('subject', 'chapter')},
        ),
    ]
