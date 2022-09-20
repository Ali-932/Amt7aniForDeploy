# -*- coding: utf-8 -*-
"""
Daily cleanup job.

Can be run as a cronjob to clean out old data from the database (only expired
sessions at the moment).
"""
from django.contrib.auth import get_user_model
from django_extensions.management.jobs import  HourlyJob
User = get_user_model()


class Job(HourlyJob):
    help = "clear unactive users"
    def execute(self):
        for i in User.objects.exclude(code=None):
            i.code=None
            i.save()

#
# class Job(DailyJob):
#     help = "Django Daily Cleanup Job"
#
#     def execute(self):
#         from django.core import management
#         management.call_command("clearsessions")