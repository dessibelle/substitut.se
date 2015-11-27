# -*- coding: utf-8 -*-

""" Unit model. """

from django.db import models
from recipes.models.ingredient import Ingredient
from django.utils.translation import ugettext as _


class Unit(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    short_name = models.CharField(max_length=8, verbose_name=_('Short name'))

    class Meta:
        app_label = 'recipes'
        verbose_name = _('Unit')

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
        verbose_name = _('Ingredient')
