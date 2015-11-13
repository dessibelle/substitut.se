# -*- coding: utf-8 -*-

""" Site views are views returning HTML """

from __future__ import absolute_import
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.templatetags.static import static
# from django.contrib.staticsfiles.templatetags.staticfiles import static
from django.shortcuts import render
from django.http import Http404
from django.core.urlresolvers import reverse
from django.conf import settings
from recipes.models.term import Term
from recipes.models.food_group import FoodGroup
from recipes.models.ingredient import Ingredient
from recipes.models.recipe import Recipe
from recipes.forms.recipe import RecipeForm
from sorl.thumbnail import get_thumbnail
# from random import randint
import logging
import mistune


# Get an instance of a logger
logger = logging.getLogger("substitut")


class NullHandler(logging.Handler):

    """Used when no logging conf is defined."""

    def emit(self, record):
        """Do nothing."""
        pass


nullhandler = logger.addHandler(NullHandler())


@cache_page(60 * 15)
def about(request):
    return render(request, 'recipes/about.html', {
        'limit': settings.PAGE_LIMIT,
        })


@cache_page(60 * 15)
def index(request):
    latest_recipes = Recipe.objects.filter(status=1).order_by('-pub_date')[:4]
    latest_recipes_with_links = []
    for recipe in latest_recipes:
        latest_recipes_with_links.append({
            'id': recipe.id,
            'name': recipe.name,
            'url': recipe.get_absolute_url(),
            'plain_url': reverse('plain_recipes', args=(recipe.id,)),
            'img_small': get_thumbnail(recipe.image, '135x135', crop='center', quality=99).url,
            'img_medium': get_thumbnail(recipe.image, '270x270', crop='center', quality=99).url,
            'img_large': get_thumbnail(recipe.image, '540x540', crop='center', quality=99).url
            })

    popular_recipes = Recipe.objects.filter(status=1).order_by('-num_votes')[:4]
    popular_recipes_with_links = []
    for recipe in popular_recipes:
        popular_recipes_with_links.append({
            'id': recipe.id,
            'name': recipe.name,
            'url': recipe.get_absolute_url(),
            'plain_url': reverse('plain_recipes', args=(recipe.id,)),
            'img_small': get_thumbnail(recipe.image, '135x135', crop='center', quality=99).url,
            'img_medium': get_thumbnail(recipe.image, '270x270', crop='center', quality=99).url,
            'img_large': get_thumbnail(recipe.image, '540x540', crop='center', quality=99).url
            })

    food_groups = FoodGroup.objects.get_food_groups()
    food_groups_grouped = {}
    for food_group in food_groups:
        ch = food_group['name'][:1].lower()
        try:
            food_groups_grouped[ch].append(food_group)
        except:
            food_groups_grouped[ch] = []
            food_groups_grouped[ch].append(food_group)
            pass

    print(food_groups_grouped)

    parallax_src = "images/site/{}.jpg"
    # index = randint(1, 6)

    return render(request, 'recipes/index.html', {
        'limit': settings.PAGE_LIMIT,
        'latest_recipes': latest_recipes_with_links,
        'popular_recipes': popular_recipes_with_links,
        'food_groups': food_groups_grouped,
        'parallax_src': static(parallax_src.format(1))
        })


@cache_page(60 * 15)
def recipes(request, lookup, slug=None):
    """Fetch a single recipe."""
    recipe = Recipe.objects.get_slug(lookup)
    if recipe and recipe['slug'] != slug:
        raise Http404

    try:
        endpoint = reverse('api_recipes', args=[recipe['id']])
    except:
        raise Http404

    return render(
        request,
        'recipes/recipes.html',
        {
            'endpoint': endpoint,
            'page_title': recipe['name'],
            'limit': settings.PAGE_LIMIT
        }
    )


@cache_page(60 * 15)
def food_groups(request, lookup, slug=None):
    food_group = FoodGroup.objects.get_slug(lookup)
    if food_group and food_group['slug'] != slug:
        raise Http404

    try:
        endpoint = reverse('api_food_groups', args=[food_group['id']])
    except:
        raise Http404

    return render(
        request,
        'recipes/recipes.html',
        {
            'endpoint': endpoint,
            'page_title': food_group['name'],
            'limit': settings.PAGE_LIMIT
        }
    )


@cache_page(60 * 15)
def ingredients(request, lookup, slug=None):
    ingredient = Ingredient.objects.get_slug(lookup)
    if not ingredient or ingredient['slug'] != slug:
        raise Http404

    try:
        endpoint = reverse('api_ingredients', args=[ingredient['id']])
    except:
        raise Http404

    return render(
        request,
        'recipes/recipes.html',
        {
            'endpoint': endpoint,
            'page_title': ingredient['name'],
            'limit': settings.PAGE_LIMIT
        }
    )


def plain_recipes(request, recipe_id):
    """ Plain html version for robots."""
    md = mistune.Markdown()
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = Ingredient.objects.with_units(recipe_id)
    obj = {
        'id': recipe.id,
        'type': Term.RECIPE,
        'name': recipe.name,
        'url': recipe.get_absolute_url(),
        'instructions': md.render(recipe.instructions),
        'img_small': get_thumbnail(recipe.image, '135x135', crop='center', quality=99).url,
        'img_medium': get_thumbnail(recipe.image, '270x270', crop='center', quality=99).url,
        'img_large': get_thumbnail(recipe.image, '540x540', crop='center', quality=99).url,
        'pub_date': unicode(recipe.pub_date),
        'description': md.render(recipe.description),
        'servings': recipe.servings,
        'status': recipe.status,
        'ingredients': ingredients['list'],
        'vote_total': 0,
        'food_groups': FoodGroup.objects.get_food_groups(recipe.id),
        'weight': ingredients['weight']
    }
    return render(request, 'recipes/plain.html', {'recipe': obj})


def recipe_form(request):
    form = RecipeForm()
    return render(request, 'recipes/form.html', {'form': form})


def bootstrap(request):
    return render(request, 'recipes/bootstrap.html')
