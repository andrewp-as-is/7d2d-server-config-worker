from django.db import models


class Restart(models.Model):
    server_id = models.IntegerField()

    class Meta:
        managed = False
