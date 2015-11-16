from __future__ import absolute_import
from django.conf.urls import url
from django.conf import settings
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from recipes.models.recipe import Recipe
from recipes.models.food_group import FoodGroup
from recipes.views import *

recipes_sitemap = {
    'queryset': Recipe.objects.filter(status=Recipe.PUBLISHED),
    'date_field': 'pub_date',
}

food_group_sitemap = {
    'queryset': FoodGroup.objects.all()
}

urlpatterns = [
    url(r'^$',
        site.index, name='index'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {
        'recipe': GenericSitemap(recipes_sitemap, priority=0.6),
        'food_group': GenericSitemap(food_group_sitemap, priority=0.5)
    }}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^recipe/(?P<recipe_id>[0-9]+)/$',
        site.plain_recipes, name='plain_recipes'),
    url(r'^recept/(?P<lookup>[a-zA-Z0-9]+)(?:/(?P<slug>[a-zA-Z0-9-]+))?$',
        site.recipes, name='recipes'),
    url(r'^kategori/(?P<lookup>[a-zA-Z0-9]+)(?:/(?P<slug>[a-zA-Z0-9-]+))?$',
        site.food_groups, name='food_groups'),
    url(r'^ingrediens/(?P<lookup>[a-zA-Z0-9]+)(?:/(?P<slug>[a-zA-Z0-9-]+))?$',
        site.ingredients, name='ingredients'),
    url(r'^skicka-in-recept/$',
        site.recipe_form, name='recipe-form'),
    url(r'^api/recipes/vote/(?P<recipe_id>[0-9]+)/$',
        api.api_vote, name='api_vote'),
    url(r'^api/recipes/(?P<recipe_id>[0-9]+)/$',
        api.api_recipes, name='api_recipes'),
    url(r'^api/ingredients/(?P<ingredient_id>[0-9]+)/$',
        api.api_ingredients, name='api_ingredients'),
    url(r'^api/terms$',
        api.api_terms, name='api_terms'),
    url(r'^api/food-groups/(?P<food_group_id>[0-9]+)/$',
        api.api_food_groups, name='api_food_groups'),
    url(r'^api/recipes/votes/(?P<recipe_id>[0-9]+)/$',
        api.api_votes, name='api_votes'),
    url(r'^om/$',
        site.about, name='about'),
    url(r'^bootstrap/$',
        site.bootstrap, name='bootstrap'),
    url(r'^media/(?P<path>.*)$',
        'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    ]
