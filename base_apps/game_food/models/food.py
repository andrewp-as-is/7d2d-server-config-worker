from django.contrib.postgres.fields import ArrayField
from django.db import models


class Food(models.Model):
    entity = models.ForeignKey('game_entity.Entity', related_name="+", on_delete=models.CASCADE,primary_key=True)
    food = models.IntegerField()
    health = models.IntegerField()
    stamina = models.IntegerField()
    water = models.IntegerField()
    dysentery = models.IntegerField()

    EconomicValue = models.IntegerField()
    Stacknumber = models.IntegerField()
    UnlockedBy = ArrayField(models.TextField())
    tags = ArrayField(models.TextField())

    class Meta:
        managed = False
