from django.db import models


class Stop(models.Model):
    server_id = models.IntegerField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
