# celery.py
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uwu_project.settings')

app = Celery('uwu_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
