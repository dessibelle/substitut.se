# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.crypto


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('lookup', models.SlugField(default=django.utils.crypto.get_random_string, unique=True, max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('energy_kj', models.FloatField(default=0, null=True, blank=True)),
                ('energy_kcal', models.FloatField(default=0, null=True, blank=True)),
                ('protein', models.FloatField(default=0, null=True, blank=True)),
                ('fat', models.FloatField(default=0, null=True, blank=True)),
                ('carbohydrates', models.FloatField(default=0, null=True, blank=True)),
                ('fibers', models.FloatField(default=0, null=True, blank=True)),
                ('salt', models.FloatField(default=0, null=True, blank=True)),
                ('water', models.FloatField(default=0, null=True, blank=True)),
                ('saturates', models.FloatField(default=0, null=True, blank=True)),
                ('monounsaturated', models.FloatField(default=0, null=True, blank=True)),
                ('trans_fat', models.FloatField(default=0, null=True, blank=True)),
                ('cholesterol', models.FloatField(default=0, null=True, blank=True)),
                ('vitamin_d', models.FloatField(default=0, null=True, blank=True)),
                ('vitamin_e', models.FloatField(default=0, null=True, blank=True)),
                ('vitamin_k', models.FloatField(default=0, null=True, blank=True)),
                ('vitamin_c', models.FloatField(default=0, null=True, blank=True)),
                ('vitamin_b6', models.FloatField(default=0, null=True, blank=True)),
                ('vitamin_b12', models.FloatField(default=0, null=True, blank=True)),
                ('iron', models.FloatField(default=0, null=True, blank=True)),
                ('lookup', models.SlugField(default=django.utils.crypto.get_random_string, unique=True, max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('instructions', models.TextField()),
                ('image', models.ImageField(upload_to=b'static/recipes/images/')),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('status', models.SmallIntegerField(choices=[(0, b'Unpublished'), (1, b'Published')])),
                ('lookup', models.SlugField(default=django.utils.crypto.get_random_string, unique=True, max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeFoodGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('food_group', models.ForeignKey(to='recipes.FoodGroup')),
                ('recipe', models.ForeignKey(to='recipes.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
                ('text', models.CharField(max_length=255)),
                ('ingredient', models.ForeignKey(to='recipes.Ingredient')),
                ('recipe', models.ForeignKey(to='recipes.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('type', models.SmallIntegerField(choices=[(0, b'Recipe'), (1, b'Ingredient'), (2, b'Tag')])),
                ('endpoint', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('short_name', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='UnitIngredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('multiplier', models.FloatField()),
                ('ingredient', models.ForeignKey(to='recipes.Ingredient')),
                ('unit', models.ForeignKey(to='recipes.Unit')),
            ],
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='unit',
            field=models.ForeignKey(to='recipes.Unit'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(to='recipes.Ingredient', through='recipes.RecipeIngredient'),
        ),
        migrations.AddField(
            model_name='foodgroup',
            name='recipes',
            field=models.ManyToManyField(to='recipes.Recipe', through='recipes.RecipeFoodGroup'),
        ),
    ]
