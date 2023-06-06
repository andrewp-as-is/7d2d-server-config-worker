__all__ = ['Translation']

from django.db import models

class Translation(models.Model):
    entity = models.ForeignKey('game_entity.Entity', related_name="+", on_delete=models.CASCADE)
    language = models.ForeignKey('game_language.Language', related_name="+", on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        managed = False
        ordering = ('entity','language')
