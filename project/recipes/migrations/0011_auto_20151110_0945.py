# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20151109_1044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipeingredient',
            old_name='order',
            new_name='sort_order',
        ),
    ]
