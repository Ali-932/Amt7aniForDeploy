# -*- coding: utf-8 -*-
"""
Daily cleanup job.

Can be run as a cronjob to clean out old data from the database (only expired
sessions at the moment).
"""
from django.contrib.auth import get_user_model
from django_extensions.management.jobs import  WeeklyJob
User = get_user_model()


class Job(WeeklyJob):
    help = "clear unactive users"
    def execute(self):
        if User.objects.filter(is_active=False):
            for i in User.objects.filter(is_active=False):
                i.delete()
            return
#
# class Job(DailyJob):
#     help = "Django Daily Cleanup Job"
#
#     def execute(self):
#         from django.core import management
#         management.call_command("clearsessions")