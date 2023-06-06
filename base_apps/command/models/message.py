__all__ = ['Message']

from django.db import models

from base_apps.utils import get_timestamp

class Message(models.Model):
    command = models.ForeignKey('command.Command', related_name="+", on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.IntegerField(default=get_timestamp)

    class Meta:
        managed = False
        ordering = ('-timestamp', )
