from django.db import models


class Empty(models.Model):
    server_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
