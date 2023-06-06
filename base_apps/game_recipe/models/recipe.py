__all__ = ['Recipe']

from django.db import models

from django.contrib.postgres.fields import ArrayField

class Recipe(models.Model):
    key = models.TextField()
    craft_area = models.TextField(null=True)
    craft_time = models.IntegerField(null=True)
    craft_tool = models.TextField(null=True)
    count = models.IntegerField()
    tags = ArrayField(models.TextField())
    ingredients = models.TextField()

    class Meta:
        managed = False
        ordering = ('key','ingredients', )

    def get_ingridients(self):
        data = {}
        for l in self.ingredients.splitlines():
            key,count = l.split(':')[0], int(l.split(':')[1])
            data[key] = count
        return data
