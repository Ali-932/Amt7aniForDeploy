# Generated by Django 4.0.6 on 2022-09-13 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0017_rename_total_right_choices_userscoring_total_right_points_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userquizzes',
            name='chapter',
        ),
        migrations.RemoveField(
            model_name='userquizzes',
            name='subject',
        ),
        migrations.AddField(
            model_name='userquizzes',
            name='quiz',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='User_quizzes', to='Home.quiz'),
        ),
    ]
