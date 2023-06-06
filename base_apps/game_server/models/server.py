from django.db import models


class Server(models.Model):
    addr = models.TextField(unique=True)
    ip = models.TextField()
    port = models.IntegerField()

    class Meta:
        managed = False
