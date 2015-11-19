# -*- coding: utf-8 -*-

""" Common functions used by both api and site. """

from recipes.models.term import Term
from recipes.models.food_group import FoodGroup
from recipes.models.ingredient import Ingredient
from recipes.models.recipe import Recipe
from sorl.thumbnail import get_thumbnail
from django.core.cache import cache
import mistune


def recipes_dict(recipe_id, format_md=True):
    """ Get recipe data for a singe recipe.

    Return:
        JSON.
    """
    cache_key = "recipes_dict_{}_{}".format(recipe_id, "true" if format_md else "false")
    output = cache.get(cache_key)
    if not output:
        recipe = Recipe.objects.get(pk=recipe_id)

        if not recipe:
            return None

        if format_md:
            md = mistune.Markdown()

        output = {
            'url': recipe.get_absolute_url(),
            'label': recipe.name,
            'data': [],
            'count': 1
        }

        ingredients = Ingredient.objects.with_units(recipe_id)

        output['data'].append({
            'id': recipe.id,
            'type': Term.RECIPE,
            'name': recipe.name,
            'url': recipe.get_absolute_url(),
            'instructions': md.render(recipe.instructions) if format_md else recipe.instructions,
            'img_small': get_thumbnail(recipe.image, '135x135', crop='center', quality=99).url,
            'img_medium': get_thumbnail(recipe.image, '270x270', crop='center', quality=99).url,
            'img_large': get_thumbnail(recipe.image, '540x540', crop='center', quality=99).url,
            'pub_date': str(recipe.pub_date),
            'description': md.render(recipe.description) if format_md else recipe.description,
            'servings': recipe.servings,
            'status': recipe.status,
            'ingredients': ingredients['list'],
            'vote_total': 0,
            'food_groups': FoodGroup.objects.get_food_groups(recipe.id),
            'weight': ingredients['weight']
        })

        cache.set(cache_key, output, 10)

    return output
