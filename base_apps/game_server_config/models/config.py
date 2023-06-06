from django.db import models


class Config(models.Model):
    server_id = models.IntegerField(primary_key=True)
    config = models.JSONField()

    class Meta:
        managed = False
