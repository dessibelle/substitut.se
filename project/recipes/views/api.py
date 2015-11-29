# -*- coding: utf-8 -*-

""" API views are views returning JSON. """

from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import Http404
from django.http import JsonResponse
from django.conf import settings
from recipes.models.term import Term
from recipes.models.food_group import FoodGroup
from recipes.models.ingredient import Ingredient
from recipes.models.recipe import Recipe
from recipes.models.vote import Vote
from recipes.views.common import recipes_dict
from sorl.thumbnail import get_thumbnail
import mistune
import logging

# Get an instance of a logger
logger = logging.getLogger("substitut")


class NullHandler(logging.Handler):

    """Used when no logging conf is defined."""

    def emit(self, record):
        """Do nothing."""
        pass


nullhandler = logger.addHandler(NullHandler())


@never_cache
@csrf_protect
def api_vote(request, recipe_id):
    """ Create a new vote object.

    Args:
        recipe_id (int): Recipe id.

    Example:
        Example response:
            {
                'status': 'ok',
                'recipe_id': 12345
            }

    Return:
        JSON. Status 'ok' on success and 'denied' on failure.
    """
    if request.method != 'POST':
        raise Http404

    vote_type = request.POST.get('type', None)
    if vote_type == 'up':
        vote_type = Vote.VOTE_UP
    elif vote_type == 'down':
        vote_type = Vote.VOTE_DOWN
    else:
        raise Http404

    try:
        Vote.objects.create_vote(request, recipe_id, vote_type)
        output = {'status': 'ok', 'recipe_id': recipe_id}
    except Exception:
        # UNIQUE constraint failed
        output = {'status': 'denied', 'recipe_id': recipe_id}
        pass

    return JsonResponse(output)


@never_cache
def api_votes(request, recipe_id):
    """ Get number of votes for current recipe.

    Args:
        recipe_id (int): Recipe id.

    Example:
        Example response:
            {
                'recipe_id': 1,
                'votes': 99
            }

    Return:
        JSON.
    """
    votes_total = Vote.objects.get_votes(recipe_id)
    output = {
        'recipe_id': recipe_id,
        'votes': votes_total
    }
    return JsonResponse(output)


@cache_page(60 * 15)
@csrf_protect
def api_terms(request):
    """ Get terms for autocomplete.

    Example:
        Example response:
            {
                'id': 1,
                'type': 1,
                'name': 'example name',
                'endpoint': '/endpoint/url'
            }

    Return:
        JSON.
    """
    output = {}
    if request.method == "POST":
        if u'term' in request.POST:
            term = request.POST[u'term']
            output = Term.objects.lookup(term)
    return JsonResponse(output, safe=False)


@cache_page(60 * 15)
@csrf_protect
def api_recipes(request, recipe_id):
    """ Get recipe data for a singe recipe."""
    output = recipes_dict(recipe_id)
    if not output:
        raise Http404
    return JsonResponse(output)


@csrf_protect
def api_ingredients(request, ingredient_id):
    ingredient = Ingredient.objects.get(pk=ingredient_id)
    if not ingredient:
        raise Http404

    if 'o' in request.POST:
        offset = int(request.POST['o'])
        if offset < 0:
            offset = 0
    else:
        offset = 0

    recipes = Recipe.objects.filter(ingredients=ingredient_id)\
        .order_by('-score')[offset:offset + settings.PAGE_LIMIT]

    output = {
        'url': ingredient.get_absolute_url(),
        'label': ingredient.name,
        'data': [],
        'count': 0
    }
    md = mistune.Markdown()
    for recipe in recipes:
        ingredients = Ingredient.objects.with_units(recipe.id)
        output['data'].append(
            {
                'id': recipe.id,
                'type': Term.RECIPE,
                'name': recipe.name,
                'url': recipe.get_absolute_url(),
                'instructions': md.render(recipe.instructions),
                'img_small': get_thumbnail(recipe.image, '135x135', crop='center', quality=99).url,
                'img_medium': get_thumbnail(recipe.image, '270x270', crop='center', quality=99).url,
                'img_large': get_thumbnail(recipe.image, '540x540', crop='center', quality=99).url,
                'pub_date': str(recipe.pub_date),
                'description': md.render(recipe.description),
                'servings': recipe.servings,
                'status': recipe.status,
                'ingredients': ingredients['list'],
                'vote_total': 0,
                'food_groups': FoodGroup.objects.get_food_groups(recipe.id),
                'weight': ingredients['weight']
            }
        )
        output['count'] += 1

    return JsonResponse(output)


@csrf_protect
@cache_page(60 * 15)
def api_food_groups(request, food_group_id):

    if 'o' in request.POST:
        offset = int(request.POST['o'])
        if offset < 0:
            offset = 0
    else:
        offset = 0

    recipes = Recipe.objects.filter(foodgroup=food_group_id)\
        .order_by('-score')[offset:offset + settings.PAGE_LIMIT]

    food_group = FoodGroup.objects.get(pk=food_group_id)

    output = {
        'url': food_group.get_absolute_url(),
        'label': food_group.name,
        'data': [],
        'count': 0
    }
    md = mistune.Markdown()
    for recipe in recipes:
        ingredients = Ingredient.objects.with_units(recipe.id)
        output['data'].append(
            {
                'id': recipe.id,
                'type': Term.RECIPE,
                'name': recipe.name,
                'url': recipe.get_absolute_url(),
                'instructions': md.render(recipe.instructions),
                'description': md.render(recipe.description),
                'servings': recipe.servings,
                'img_small': get_thumbnail(recipe.image, '135x135', crop='center', quality=99).url,
                'img_medium': get_thumbnail(recipe.image, '270x270', crop='center', quality=99).url,
                'img_large': get_thumbnail(recipe.image, '540x540', crop='center', quality=99).url,
                'pub_date': str(recipe.pub_date),
                'status': recipe.status,
                'ingredients': ingredients['list'],
                'vote_total': 0,
                'food_groups': FoodGroup.objects.get_food_groups(recipe.id),
                'weight': ingredients['weight']
            }
        )
        output['count'] += 1

    return JsonResponse(output)


@csrf_protect
@cache_page(60 * 15)
def api_term(request):
    output = {}
    if request.method == "POST":
        if 'term' in request.POST:
            term = request.POST['term']
            output = Term.objects.lookup(term)
    return JsonResponse(output, safe=False)
