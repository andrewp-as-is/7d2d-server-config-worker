__all__ = ['CallDuration',]

from django.db import models

class CallDuration(models.Model):
    command = models.ForeignKey('command.Command', related_name="+", on_delete=models.CASCADE)
    seconds = models.FloatField()

    class Meta:
        managed = False
