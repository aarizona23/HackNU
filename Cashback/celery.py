from celery import Celery
from celery.schedules import crontab
import os 
app = Celery('Cashback')
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HackNU.settings')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
from celery.schedules import crontab

app.conf.beat_schedule = {
    'task-name': {
        'task': 'your_project.tasks.task_function',
        'schedule': crontab(minute=0, hour=0),  # Run daily at midnight
    },
}