from django.db import models


class TimeStart(models.Model):
    server_id = models.IntegerField()

    class Meta:
        managed = False
