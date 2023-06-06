from django.db import models


class Downtime(models.Model):
    server_id = models.IntegerField()
    started_at = models.IntegerField()
    ended_at = models.IntegerField()

    class Meta:
        managed = False
