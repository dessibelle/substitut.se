# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20151004_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='num_votes',
            field=models.IntegerField(default=0),
        ),
    ]
