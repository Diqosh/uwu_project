# tasks.py
from celery import shared_task
from .models import Notification

@shared_task
def send_notification_async(notification_id):
    try:
        notification = Notification.objects.get(pk=notification_id)
        notification.send()
    except Notification.DoesNotExist:
        # Handle the case where the notification with the given ID doesn't exist
        pass
