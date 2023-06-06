__all__ = ['Error',]

from django.db import models

from base_apps.utils import get_timestamp

class Error(models.Model):
    command = models.ForeignKey('command.Command', related_name="+", on_delete=models.CASCADE)
    exc_type = models.TextField()
    exc_message = models.TextField()
    exc_traceback = models.TextField()
    timestamp = models.IntegerField(default=get_timestamp)

    class Meta:
        managed = False
        ordering = ('-timestamp', )
