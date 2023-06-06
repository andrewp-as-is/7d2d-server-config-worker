from django.db import models


class Timestamp(models.Model):
    server_id = models.IntegerField(primary_key=True)
    timestamp = models.IntegerField()

    class Meta:
        managed = False
