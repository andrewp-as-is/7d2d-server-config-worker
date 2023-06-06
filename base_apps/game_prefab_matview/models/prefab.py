from django.contrib.postgres.fields import ArrayField
from django.db import models
from base_apps.game_prefab.models import AbstractPrefab


class Prefab(AbstractPrefab):
    description = models.TextField()

    class Meta:
        managed = False
