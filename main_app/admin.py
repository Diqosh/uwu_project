from django.contrib import admin
from .models import User, Device, Notification, NotificationTemplate

admin.site.register(User)
admin.site.register(Device)
admin.site.register(NotificationTemplate)


def send_notifications(modeladmin, request, queryset):
    for notification in queryset:
        notification.send()

send_notifications.short_description = "Send selected notifications"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    actions = [send_notifications]
