# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_auto_20151110_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to=b'original', blank=True),
        ),
    ]
