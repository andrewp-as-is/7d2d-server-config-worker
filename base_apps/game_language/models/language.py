__all__ = ['Language']

from django.db import models

class Language(models.Model):
    name = models.TextField(unique=True)
    code = models.TextField(unique=True)

    class Meta:
        managed = False
        ordering = ('name', )
