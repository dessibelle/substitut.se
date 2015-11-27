# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.crypto
import django.utils.timezone
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_auto_20151121_1628'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foodgroup',
            options={'verbose_name': 'Food group'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Ingredient'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'verbose_name': 'Recipe'},
        ),
        migrations.AlterModelOptions(
            name='recipefoodgroup',
            options={'verbose_name': 'Food group'},
        ),
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'verbose_name': 'Ingredient'},
        ),
        migrations.AlterModelOptions(
            name='term',
            options={'verbose_name': 'Term'},
        ),
        migrations.AlterModelOptions(
            name='unit',
            options={'verbose_name': 'Unit'},
        ),
        migrations.AlterModelOptions(
            name='unitingredient',
            options={'verbose_name': 'Ingredient'},
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='num_votes',
        ),
        migrations.AddField(
            model_name='recipe',
            name='score',
            field=models.IntegerField(verbose_name='Votes', default=0),
        ),
        migrations.AddField(
            model_name='vote',
            name='vote',
            field=models.SmallIntegerField(verbose_name='Vote', choices=[(1, 'Up'), (-1, 'Down')], default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='foodgroup',
            name='lookup',
            field=models.SlugField(unique=True, max_length=13, default=django.utils.crypto.get_random_string, verbose_name='Hash'),
        ),
        migrations.AlterField(
            model_name='foodgroup',
            name='name',
            field=models.CharField(verbose_name='Namn', max_length=200),
        ),
        migrations.AlterField(
            model_name='foodgroup',
            name='recipes',
            field=models.ManyToManyField(verbose_name='Recipes', to='recipes.Recipe', through='recipes.RecipeFoodGroup'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='carbohydrates',
            field=models.FloatField(verbose_name='Carbohydrates', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='cholesterol',
            field=models.FloatField(verbose_name='Cholesterol', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='energy_kcal',
            field=models.FloatField(verbose_name='Enery (kcal)', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='energy_kj',
            field=models.FloatField(verbose_name='Energy (kj)', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='fat',
            field=models.FloatField(verbose_name='Fat', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='fibers',
            field=models.FloatField(verbose_name='Fibers', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='iron',
            field=models.FloatField(verbose_name='Iron', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='lookup',
            field=models.SlugField(unique=True, max_length=13, default=django.utils.crypto.get_random_string, verbose_name='Hash'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='monounsaturated',
            field=models.FloatField(verbose_name='Monounsaturated', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(verbose_name='Namn', max_length=128),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='protein',
            field=models.FloatField(verbose_name='Protein', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='salt',
            field=models.FloatField(verbose_name='Salt', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='saturates',
            field=models.FloatField(verbose_name='Saturates', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='trans_fat',
            field=models.FloatField(verbose_name='Trans fat', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='vitamin_b12',
            field=models.FloatField(verbose_name='Vitamin B12', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='vitamin_b6',
            field=models.FloatField(verbose_name='Vitamin B6', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='vitamin_c',
            field=models.FloatField(verbose_name='Vitamin C', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='vitamin_d',
            field=models.FloatField(verbose_name='Vitamin D', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='vitamin_e',
            field=models.FloatField(verbose_name='Vitamin E', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='vitamin_k',
            field=models.FloatField(verbose_name='Vitamin K', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='water',
            field=models.FloatField(verbose_name='Water', blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=sorl.thumbnail.fields.ImageField(verbose_name='Bild', upload_to='original', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(verbose_name='Ingredients', to='recipes.Ingredient', through='recipes.RecipeIngredient'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='instructions',
            field=models.TextField(verbose_name='Instructions'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='lookup',
            field=models.SlugField(unique=True, max_length=13, default=django.utils.crypto.get_random_string, verbose_name='Hash'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(verbose_name='Namn', max_length=200),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Last modified', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='servings',
            field=models.SmallIntegerField(verbose_name='Servings', default=4),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='status',
            field=models.SmallIntegerField(verbose_name='Status', choices=[(0, 'Unpublished'), (1, 'Published')]),
        ),
        migrations.AlterField(
            model_name='recipefoodgroup',
            name='food_group',
            field=models.ForeignKey(verbose_name='Food group', to='recipes.FoodGroup'),
        ),
        migrations.AlterField(
            model_name='recipefoodgroup',
            name='recipe',
            field=models.ForeignKey(verbose_name='Recipe', to='recipes.Recipe'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.FloatField(verbose_name='Amount', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(verbose_name='Ingredient', to='recipes.Ingredient'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(verbose_name='Recipe', to='recipes.Recipe'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='sort_order',
            field=models.IntegerField(verbose_name='Sort order', default=0),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='text',
            field=models.CharField(verbose_name='Text', max_length=255),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='unit',
            field=models.ForeignKey(blank=True, verbose_name='Unit', to='recipes.Unit', null=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='endpoint',
            field=models.CharField(verbose_name='Endpoint URL', max_length=255),
        ),
        migrations.AlterField(
            model_name='term',
            name='name',
            field=models.CharField(verbose_name='Namn', max_length=128),
        ),
        migrations.AlterField(
            model_name='term',
            name='type',
            field=models.SmallIntegerField(verbose_name='Type', choices=[(0, 'Recipe'), (1, 'Ingredient'), (2, 'Tag')]),
        ),
        migrations.AlterField(
            model_name='unit',
            name='name',
            field=models.CharField(verbose_name='Namn', max_length=64),
        ),
        migrations.AlterField(
            model_name='unit',
            name='short_name',
            field=models.CharField(verbose_name='Short name', max_length=8),
        ),
        migrations.AlterField(
            model_name='vote',
            name='created',
            field=models.DateField(verbose_name='Created', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='vote',
            name='ip_address',
            field=models.GenericIPAddressField(verbose_name='IP Address'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='recipe',
            field=models.ForeignKey(verbose_name='Recipe', to='recipes.Recipe'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='user_agent',
            field=models.CharField(verbose_name='User Agent', max_length=128),
        ),
    ]
