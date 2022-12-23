from datetime import datetime
from django_celery_beat.models import PeriodicTask,CrontabSchedule
import random
import json

class CeleryService():
    

    def create_new_task(self,**kwargs):
        """
        params(dict:kwargs)
        creates new crontab scheduled task 
        """
        schedule,created = CrontabSchedule.objects.get_or_create(
                       hour = kwargs.get('hour'),
                       minute = kwargs.get('minute'),
                       day_of_month = kwargs.get('day_of_month'),
                       month_of_year = kwargs.get('month_of_year')
                    )

        return schedule
    
    def create_periodic_task(self,**kwargs):
        """
        params(dict:kwargs)
        creates new periodic scheduled task 
        """
        PeriodicTask.objects.create(
                        crontab = kwargs.get('crontab'),
                        name = kwargs.get("name"),
                        task = kwargs.get("task"),
                        kwargs = kwargs.get("kwargs")
                    )
        print('created')
        return True