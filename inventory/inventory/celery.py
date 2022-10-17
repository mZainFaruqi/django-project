from __future__ import  absolute_import, unicode_literals
import  os

from celery import  Celery
from django.conf import  settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory.settings')

app = Celery("inventory")
app.conf.enable_utc = False

app.conf.update(timezone='Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

# CELERY Beat Settings
app.conf.beat_schedule = {
        'some_name' : {
            'task' : 'products.tasks.test_func',
            'schedule': crontab(minute="*/2"),
           # 'args'
        }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')