# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20151004_1636'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('recipe', 'created', 'ip_address', 'user_agent')]),
        ),
        migrations.AlterIndexTogether(
            name='vote',
            index_together=set([]),
        ),
    ]
