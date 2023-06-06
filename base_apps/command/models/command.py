__all__ = ['Command',]

from django.db import models

class Command(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        managed = False
