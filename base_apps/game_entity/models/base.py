from django.db import models


class AbstractEntity(models.Model):
    key = models.TextField(unique=True)

    class Meta:
        managed = False
