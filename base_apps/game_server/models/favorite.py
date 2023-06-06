from django.db import models


class Favorite(models.Model):
    server_id = models.IntegerField()
    steam_id = models.IntegerField()

    class Meta:
        managed = False
        unique_together = [('server_id','steam_id')]
