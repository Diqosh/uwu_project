# tasks.py
from celery import shared_task
from .models import Notification

@shared_task
def send_notification_async(notification_id):
    try:
        notification = Notification.objects.get(pk=notification_id)
        notification.send()
    except Notification.DoesNotExist:
      raise ValueError(f"Error: Notification with id '{notification_id}' does not exist")
