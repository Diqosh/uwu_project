from django.contrib import admin

from main_app.froms import NotificationTemplateForm
from .models import User, Device, Notification, NotificationTemplate

admin.site.register(User)
admin.site.register(Device)


def send_notifications(modeladmin, request, queryset):
    for notification in queryset:
        notification.send()

send_notifications.short_description = "Send selected notifications"


from .tasks import send_notification_async

def send_notifications_async(modeladmin, request, queryset):
    for notification in queryset:
      print(notification.id)
      send_notification_async.apply_async(notification.id)

send_notifications_async.short_description = "Send selected notifications asynchronously"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    actions = [send_notifications, send_notification_async]

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    form = NotificationTemplateForm
