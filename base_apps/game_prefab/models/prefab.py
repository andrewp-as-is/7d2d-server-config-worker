from django.contrib.postgres.fields import ArrayField
from django.db import models


class AbstractPrefab(models.Model):
    name = models.TextField(unique=True)
    DifficultyTier = models.IntegerField(null=True)
    QuestTags = ArrayField(models.TextField())
    Tags = ArrayField(models.TextField())
    PrefabSize = models.TextField(null=True) # page only

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return '/prefabs/%s' % self.name

class Prefab(AbstractPrefab):

    class Meta:
        managed = False
