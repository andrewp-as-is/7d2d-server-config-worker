from django.db import models


class PrefabBlock(models.Model):
    prefab_id = models.IntegerField()
    block_id = models.IntegerField()
    count = models.IntegerField()

    class Meta:
        managed = False
        unique_together = [('prefab_id','block_id')]
