# -*- coding: utf-8 -*-

""" Ingredient model. """

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from recipes.models.recipe import Recipe


class IngredientManager(models.Manager):
    def with_units(self, recipe_id):
        from django.db import connection

        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                i.name,
                i.energy_kj,
                i.energy_kcal,
                i.protein,
                i.fat,
                i.carbohydrates,
                i.fibers,
                i.salt,
                i.water,
                i.saturates,
                i.monounsaturated,
                i.trans_fat,
                i.cholesterol,
                i.vitamin_d,
                i.vitamin_e,
                i.vitamin_k,
                i.vitamin_c,
                i.vitamin_b6,
                i.vitamin_b12,
                i.iron,
                ui.multiplier,
                u.name,
                u.short_name,
                ri.amount,
                ri.text
            FROM
                recipes_ingredient i
            INNER JOIN
                recipes_recipeingredient ri ON ri.ingredient_id = i.id
            LEFT JOIN
                recipes_unit u ON u.id = ri.unit_id
            LEFT JOIN
                recipes_unitingredient ui ON ui.ingredient_id = i.id
            AND
                ui.unit_id = u.id
            WHERE
                ri.recipe_id = %s
            ORDER BY
                ri.sort_order ASC""", [recipe_id])
        result = {
            'weight': 0,
            'list': []
        }
        for row in cursor.fetchall():
            # calculate multiplier
            multiplier = row[20] or 0
            amount = row[23] or 0
            weight = multiplier * amount
            result['weight'] += weight * 100
            result['list'].append({
                "name": row[0],
                "energy_kj": row[1] * weight,
                "energy_kcal": row[2] * weight,
                "protein": row[3] * weight,
                "fat": row[4] * weight,
                "carbohydrates": row[5] * weight,
                "fibers": row[6] * weight,
                "salt": row[7] * weight,
                "water": row[8] * weight,
                "saturates": row[9] * weight,
                "monounsaturated": row[10] * weight,
                "trans_fat": row[11] * weight,
                "cholesterol": row[12] * weight,
                "vitamin_d": row[13] * weight,
                "vitamin_e": row[14] * weight,
                "vitamin_k": row[15] * weight,
                "vitamin_c": row[16] * weight,
                "vitamin_b6": row[17] * weight,
                "vitamin_b12": row[18] * weight,
                "iron": row[19] * weight,
                "multiplier": row[20],
                "unit": row[21],
                "unit_short": row[22],
                "amount": row[23],
                "text": row[24]
                })
        return result

    def get_index(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT DISTINCT
                ri.ingredient_id,
                ri.text
            FROM
                recipes_recipeingredient ri
            INNER JOIN
                recipes_ingredient i ON ri.ingredient_id = i.id
            INNER JOIN
                recipes_recipe r ON ri.recipe_id = r.id
            WHERE
                r.status = %s""", [Recipe.PUBLISHED])
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
        cursor.execute("""
            SELECT
                id,
                name
            FROM
                recipes_ingredient
            WHERE
                lookup = %s""", [lookup])

        result = cursor.fetchone()
        try:
            return {
                'id': result[0],
                'name': result[1],
                'slug': slugify(result[1])
            }
        except:
            return {}


class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    energy_kj = models.FloatField(default=0, blank=True, null=True)
    energy_kcal = models.FloatField(default=0, blank=True, null=True)
    protein = models.FloatField(default=0, blank=True, null=True)
    fat = models.FloatField(default=0, blank=True, null=True)
    carbohydrates = models.FloatField(default=0, blank=True, null=True)
    fibers = models.FloatField(default=0, blank=True, null=True)
    salt = models.FloatField(default=0, blank=True, null=True)
    water = models.FloatField(default=0, blank=True, null=True)
    saturates = models.FloatField(default=0, blank=True, null=True)
    monounsaturated = models.FloatField(default=0, blank=True, null=True)
    trans_fat = models.FloatField(default=0, blank=True, null=True)
    cholesterol = models.FloatField(default=0, blank=True, null=True)
    vitamin_d = models.FloatField(default=0, blank=True, null=True)
    vitamin_e = models.FloatField(default=0, blank=True, null=True)
    vitamin_k = models.FloatField(default=0, blank=True, null=True)
    vitamin_c = models.FloatField(default=0, blank=True, null=True)
    vitamin_b6 = models.FloatField(default=0, blank=True, null=True)
    vitamin_b12 = models.FloatField(default=0, blank=True, null=True)
    iron = models.FloatField(default=0, blank=True, null=True)
    objects = IngredientManager()
    lookup = models.SlugField(
        unique=True,
        default=get_random_string,
        max_length=13,
    )

    class Meta:
        app_label = 'recipes'

    @models.permalink
    def get_absolute_url(self):
        return ("ingredients", [self.lookup, self.slug()])

    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains",)
