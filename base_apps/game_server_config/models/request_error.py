from django.db import models


class RequestError(models.Model):
    server_id = models.IntegerField()
    exc_type = models.TextField()

    class Meta:
        managed = False
