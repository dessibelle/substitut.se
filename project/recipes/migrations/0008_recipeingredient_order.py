# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20151031_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeingredient',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
