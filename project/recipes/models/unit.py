from django.db import models
from ingredient import Ingredient


class Unit(models.Model):
    name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=8)

    class Meta:
        app_label = 'recipes'

    def __str__(self):
        return self.short_name

    def __unicode__(self):
        return self.short_name


# used to multiply ingredient amount depending on unit
class UnitIngredient(models.Model):
    unit = models.ForeignKey(Unit)
    ingredient = models.ForeignKey(Ingredient)
    multiplier = models.FloatField()

    class Meta:
        app_label = 'recipes'
