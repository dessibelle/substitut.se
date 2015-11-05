# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20151019_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='unit',
            field=models.ForeignKey(blank=True, to='recipes.Unit', null=True),
        ),
    ]
