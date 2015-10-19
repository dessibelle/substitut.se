# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20150929_1958'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateField(default=django.utils.timezone.now)),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.CharField(max_length=128)),
                ('recipe', models.ForeignKey(to='recipes.Recipe')),
            ],
        ),
        migrations.AlterIndexTogether(
            name='vote',
            index_together=set([('recipe', 'created', 'ip_address', 'user_agent')]),
        ),
    ]
