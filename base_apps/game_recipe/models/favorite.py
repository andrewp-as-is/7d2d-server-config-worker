__all__ = ['Favorite']

from django.db import models

class Favorite(models.Model):
    steam_id = models.IntegerField()
    recipe_id = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('steam_id','recipe_id',)
        unique_together = [('steam_id','recipe_id')]
