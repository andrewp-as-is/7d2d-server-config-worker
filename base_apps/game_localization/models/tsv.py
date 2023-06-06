__all__ = ['Tsv']

from django.db import models

class Tsv(models.Model):
    entity = models.ForeignKey('game_entity.Entity', related_name="+", on_delete=models.CASCADE)
    language = models.ForeignKey('game_language.Language', related_name="+", on_delete=models.CASCADE)
    tsv = models.TextField()

    class Meta:
        managed = False
        ordering = ('entity','language')
