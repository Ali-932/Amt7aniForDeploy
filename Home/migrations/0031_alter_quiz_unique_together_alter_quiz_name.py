# Generated by Django 4.0.6 on 2022-09-16 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0030_remove_question_quiz_question_chapter_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='quiz',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
