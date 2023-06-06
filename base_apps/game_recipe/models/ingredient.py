__all__ = ['Ingredient']

from django.db import models

class Ingredient(models.Model):
    recipe = models.ForeignKey('Recipe', related_name="+", on_delete=models.CASCADE)
    key = models.TextField()
    count = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('recipe', 'key',)
