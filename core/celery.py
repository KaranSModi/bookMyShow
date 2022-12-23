from __future__ import absolute_import,unicode_literals
import os
from celery.schedules import crontab
from celery import Celery   
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','core.settings')

app = Celery('core')
# app.conf.enable_utc = False
# app.conf.update(timezone='Asia/Kolkata')
app.config_from_object(settings,namespace='CELERY')



app.conf.beat_schedule = {
    #Scheduler Name
    'print-test-task': {
        # Task Name (Name Specified in Decorator)
        'task': 'revert_seats_func',  
        # Schedule      
        'schedule': 30.0
        # Function Arguments 
    #    'args': (request) 
    },}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print("hello "+ self.request)