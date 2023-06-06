from django.db import models


class Job(models.Model):
    server_id = models.TextField(primary_key=True)

    class Meta:
        managed = False
