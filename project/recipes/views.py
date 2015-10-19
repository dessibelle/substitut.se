from django.views.decorators.cache import cache_page, never_cache
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from models.term import Term
from models.food_group import FoodGroup
from models.ingredient import Ingredient
from models.recipe import Recipe
from models.vote import Vote
import simplejson
import mistune


@never_cache
def index(request):
    return render(request, 'recipes/index.html')


@never_cache
def api_vote(request, recipe_id):
    try:
        Vote.objects.create_vote(request, recipe_id)
        output = simplejson.dumps({'status': 'ok'})
    except Exception as e:
        print(e)
        # UNIQUE constraint failed
        output = simplejson.dumps({'status': 'denied'})
        pass

    return HttpResponse(output)


@never_cache
def api_votes(request, recipe_id):
    votes_total = Vote.objects.get_votes(recipe_id)
    output = {'recipe_id': recipe_id, 'votes': votes_total}
    return HttpResponse(simplejson.dumps(output))


def recipes(request, lookup, slug=None):
    recipe = Recipe.objects.get_slug(lookup)
    if recipe and recipe['slug'] != slug:
        raise Http404

    try:
        endpoint = reverse('api_recipes', args=[recipe['id']])
    except:
        raise Http404

    return render(request, 'recipes/recipes.html', {'endpoint': endpoint})


def food_groups(request, lookup, slug=None):
    food_group = FoodGroup.objects.get_slug(lookup)
    if food_group and food_group['slug'] != slug:
        raise Http404

    try:
        endpoint = reverse('api_food_groups', args=[food_group['id']])
    except:
        raise Http404

    return render(request, 'recipes/recipes.html', {'endpoint': endpoint})


def ingredients(request, lookup, slug=None):
    ingredient = Ingredient.objects.get_slug(lookup)
    if not ingredient or ingredient['slug'] != slug:
        raise Http404

    try:
        endpoint = reverse('api_ingredients', args=[ingredient['id']])
    except:
        raise Http404

    return render(request, 'recipes/recipes.html', {'endpoint': endpoint})


@cache_page(60 * 15)
def api_terms(request):
    """ Get terms for autocomplete
    """
    if request.method == "GET":
        if u'term' in request.GET:
            term = request.GET[u'term']
            results = Term.objects.lookup(term)
    output = simplejson.dumps(results)
    return HttpResponse(output) # todo return json header


@cache_page(60 * 15)
def api_recipes(request, recipe_id):
    md = mistune.Markdown()
    _recipe = get_object_or_404(Recipe, pk=recipe_id)
    result = {
        'url': _recipe.get_absolute_url(),
        'label': _recipe.name,
        'data': [],
        'count': 1
    }
    ingredients = Ingredient.objects.with_units(recipe_id)
    result['data'].append({
        'id': _recipe.id,
        'type': Term.RECIPE,
        'name': _recipe.name,
        'url': _recipe.get_absolute_url(),
        'instructions': md.render(_recipe.instructions),
        'image': unicode(_recipe.image),
        'pub_date': unicode(_recipe.pub_date),
        'description': md.render(_recipe.description),
        'servings': _recipe.servings,
        'status': _recipe.status,
        'ingredients': ingredients['list'],
        'vote_total': 0,
        'weight': ingredients['weight']
    })

    output = simplejson.dumps(result)
    return HttpResponse(output) # todo return json header


@cache_page(60 * 15)
def api_ingredients(request, ingredient_id):
    ingredient = Ingredient.objects.get(pk=ingredient_id)
    if not ingredient:
        raise Http404

    recipes = Recipe.objects.filter(ingredients__in=[ingredient_id]).order_by('-num_votes')

    result = {
        'url': ingredient.get_absolute_url(),
        'label': ingredient.name,
        'data': [],
        'count': 0
    }
    md = mistune.Markdown()
    for recipe in recipes:
        ingredients = Ingredient.objects.with_units(recipe.id)
        result['data'].append(
            {
                'id': recipe.id,
                'type': Term.RECIPE,
                'name': recipe.name,
                'url': recipe.get_absolute_url(),
                'instructions': md.render(recipe.instructions),
                'image': unicode(recipe.image),
                'pub_date': unicode(recipe.pub_date),
                'description': md.render(recipe.description),
                'servings': recipe.servings,
                'status': recipe.status,
                'ingredients': ingredients['list'],
                'vote_total': 0,
                'weight': ingredients['weight']
            }
        )
        result['count'] += 1

    output = simplejson.dumps(result)
    return HttpResponse(output) # todo return json header


@cache_page(60 * 15)
def api_food_groups(request, food_group_id):
    recipes = Recipe.objects.filter(foodgroup__in=[food_group_id]).order_by('-num_votes')
    food_group = FoodGroup.objects.get(pk=food_group_id)

    result = {
        'url': food_group.get_absolute_url(),
        'label': food_group.name,
        'data': [],
        'count': 0
    }
    md = mistune.Markdown()
    for recipe in recipes:
        ingredients = Ingredient.objects.with_units(recipe.id)
        result['data'].append(
            {
                'id': recipe.id,
                'type': Term.RECIPE,
                'name': recipe.name,
                'url': recipe.get_absolute_url(),
                'instructions': md.render(recipe.instructions),
                'description': md.render(recipe.description),
                'servings': recipe.servings,
                'image': unicode(recipe.image),
                'pub_date': unicode(recipe.pub_date),
                'status': recipe.status,
                'ingredients': ingredients['list'],
                'vote_total': 0,
                'weight': ingredients['weight']
            }
        )
        result['count'] += 1

    output = simplejson.dumps(result)
    return HttpResponse(output) # todo return json header


@cache_page(60 * 15)
def api_term(request):
    if request.method == "GET":
        if u'term' in request.GET:
            term = request.GET[u'term']
            results = Term.objects.lookup(term)
    output = simplejson.dumps(results)
    return HttpResponse(output) # todo return json header
