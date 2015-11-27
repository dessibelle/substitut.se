# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_auto_20151110_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to='original', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Unpublished'), (1, 'Published')]),
        ),
        migrations.AlterField(
            model_name='term',
            name='type',
            field=models.SmallIntegerField(choices=[(0, 'Recipe'), (1, 'Ingredient'), (2, 'Tag')]),
        ),
    ]
