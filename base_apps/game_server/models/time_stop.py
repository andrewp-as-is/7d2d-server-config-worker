from django.db import models


class TimeStop(models.Model):
    server_id = models.IntegerField()

    class Meta:
        managed = False
