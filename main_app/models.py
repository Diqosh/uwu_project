from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    pass

class CustomGroup(Group):
    pass

class CustomPermission(Permission):
    pass

User.groups.field.remote_field.related_name = 'main_app_user_groups'
User.user_permissions.field.remote_field.related_name = 'main_app_user_permissions'
CustomGroup.user_set.field.remote_field.related_name = 'main_app_group_users'
CustomPermission.user_set.field.remote_field.related_name = 'main_app_permission_users'

class Device(models.Model):
  user = models.ForeignKey(
    User,
    verbose_name="User",
    on_delete=models.CASCADE,
    related_name="devices",
    )
  registration_id = models.TextField(verbose_name="Registration Token")
    
    
  def __str__(self):
    return f"{self.user} - {self.registration_id}"
  
class Notification(models.Model):
  user = models.ForeignKey(
      User,
      verbose_name="User",
      on_delete=models.CASCADE,
      related_name="notifications",
  )

  title = models.CharField("Title", max_length=64)
  body = models.TextField("Text", max_length=300)


  def send(self):
    from .magic import fcm_send_push

    fcm_send_push(
        ids=self.user.devices.values_list("registration_id", flat=True),
        notifaction_text=self.body + " " + self.user.username + " some text",
        title=self.title,
    )
  
  def __str__(self):
    return f"{self.user} - {self.title}"

class NotificationTemplate(models.Model):
  class KIND(models.TextChoices):
    ON_BUS_STOP = "on_bus_stop", "On Bus Stop"
    ON_SUBSCRIPTION_COMPLETION = "on_subscription_completion", "On Subscription Completion"
    GENERIC = "generic", "Generic"  

  # Most probably you will have a static map of all available objects for each kind.
  available_objects = {
      KIND.ON_BUS_STOP: {"ride":  {"pickup_bus_stop": "data"}},
      KIND.ON_SUBSCRIPTION_COMPLETION: {"subscription": 'some data'},
  }

  kind = models.CharField(
      _("Kind"),
      max_length=64,
      choices=KIND.choices,
      default=KIND.GENERIC,
  )
  title = models.TextField("Title")
  body = models.TextField("Text")

  def send(self, user, **kwargs):
        if self.kind in self.available_objects:
            required_objects = self.available_objects[self.kind].keys()
            missing_objects = set(required_objects) - set(kwargs.keys())
            if missing_objects:
                raise ValueError(f"Missing required objects for kind '{self.kind}': {', '.join(missing_objects)}")
        else:
            raise ValueError(f"Invalid kind: '{self.kind}'")

        title = self.title
        body = self.body

        Notification.objects.create(user=user, title=title, body=body)
  
  def __str__(self):
    return f"{self.kind} - {self.title}"
