from django.contrib.postgres.fields import ArrayField
from django.db import models


class Block(models.Model):
    name = models.TextField(unique=True)
    DescriptionKey = models.TextField(unique=True)
    Tags = ArrayField(models.TextField())
    FilterTags = ArrayField(models.TextField())
    CustomIcon = models.TextField(null=True)
    CustomIconTint = models.TextField(null=True)
    EconomicValue = models.IntegerField(null=True)
    Material = models.TextField(null=True)
    MaxDamage = models.IntegerField(null=True)
    NoScrapping = models.BooleanField(null=True)
    Stacknumber = models.IntegerField(null=True)
    SellableToTrader = models.BooleanField(null=True)
    TintColor = models.TextField(null=True)
    # repair_tools = models.TextField(null=True)
    UnlockedBy = ArrayField(models.TextField())

    class Meta:
        managed = False
