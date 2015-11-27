# -*- coding: utf-8 -*-

""" Recipe model. """

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from sorl.thumbnail import ImageField
from django.utils.translation import ugettext as _


class RecipeManager(models.Manager):
    def lookup(self, term):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, name FROM recipes_recipe WHERE name LIKE %s ORDER BY name",
            ["%%{}%%".format(term)]
        )
        result_list = []
        for row in cursor.fetchall():
            result_list.append({
                'id': row[0],
                'name': row[1]
            })
        return result_list

    def get_index(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, name FROM recipes_recipe WHERE status = %s",
            [Recipe.PUBLISHED]
        )
        result_list = []
        for row in cursor.fetchall():
            result_list.append({
                'id': row[0],
                'name': row[1]
            })
        return result_list

    def get_slug(self, lookup):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, name FROM recipes_recipe WHERE lookup = %s AND status = %s",
            [lookup, Recipe.PUBLISHED]
        )

        result = cursor.fetchone()
        try:
            return {
                'id': result[0],
                'name': result[1],
                'slug': slugify(result[1])
            }
        except:
            return {}


class Recipe(models.Model):
    UNPUBLISHED = 0
    PUBLISHED = 1
    STATUS_CHOICES = (
        (UNPUBLISHED, 'Unpublished'),
        (PUBLISHED, 'Published'),
    )
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    instructions = models.TextField(verbose_name=_('Instructions'))
    image = ImageField(upload_to='original', blank=True, null=True, verbose_name=_('Image'))
    pub_date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_('Last modified'))
    status = models.SmallIntegerField(choices=STATUS_CHOICES, verbose_name=_('Status'))
    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient', verbose_name=_('Ingredients'))
    servings = models.SmallIntegerField(default=4, verbose_name=_('Servings'))
    objects = RecipeManager()
    score = models.IntegerField(default=0, verbose_name=_('Votes'))
    lookup = models.SlugField(
        unique=True,
        default=get_random_string,
        max_length=13,
        verbose_name=_('Hash')
    )

    class Meta:
        app_label = 'recipes'
        verbose_name = _('Recipe')

    @models.permalink
    def get_absolute_url(self):
        return ("recipes", [self.lookup, self.slug()])

    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class RecipeFoodGroup(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name=_('Recipe'))
    food_group = models.ForeignKey('FoodGroup', verbose_name=_('Food group'))

    class Meta:
        app_label = 'recipes'
        verbose_name = _('Food group')


class RecipeIngredient(models.Model):
    unit = models.ForeignKey('Unit', null=True, blank=True, verbose_name=_('Unit'))
    ingredient = models.ForeignKey('Ingredient', verbose_name=_('Ingredient'))
    recipe = models.ForeignKey(Recipe, verbose_name=_('Recipe'))
    amount = models.FloatField(null=True, blank=True, verbose_name=_('Amount'))
    text = models.CharField(max_length=255, verbose_name=_('Text'))
    sort_order = models.IntegerField(default=0, verbose_name=_('Sort order'))

    class Meta:
        app_label = 'recipes'
        verbose_name = _('Ingredient')
