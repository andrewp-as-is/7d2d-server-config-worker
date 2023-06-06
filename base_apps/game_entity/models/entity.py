from django.db import models


class Entity(models.Model):
    key = models.TextField(unique=True)
    custom_icon = models.TextField(null=True)

    class Meta:
        managed = False
