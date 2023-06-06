from django.db import models


class Discord(models.Model):
    server_id = models.IntegerField(primary_key=True)
    url = models.TextField()

    class Meta:
        managed = False
