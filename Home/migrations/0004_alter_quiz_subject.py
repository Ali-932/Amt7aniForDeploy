# Generated by Django 4.0.6 on 2022-09-09 18:03

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_alter_quiz_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='subject',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field='stage', chained_model_field='stages', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quiz_subject', to='Home.subjects'),
        ),
    ]
