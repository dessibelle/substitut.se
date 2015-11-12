from __future__ import absolute_import
from django.conf.urls import url
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$',
        views.site.index, name='index'),
    url(r'^recept/(?P<lookup>[a-zA-Z0-9]+)(?:/(?P<slug>[a-zA-Z0-9-]+))?$',
        views.site.recipes, name='recipes'),
    url(r'^kategori/(?P<lookup>[a-zA-Z0-9]+)(?:/(?P<slug>[a-zA-Z0-9-]+))?$',
        views.site.food_groups, name='food_groups'),
    url(r'^ingrediens/(?P<lookup>[a-zA-Z0-9]+)(?:/(?P<slug>[a-zA-Z0-9-]+))?$',
        views.site.ingredients, name='ingredients'),
    url(r'^skicka-in-recept/$',
        views.site.recipe_form, name='recipe-form'),
    url(r'^api/recipes/vote/(?P<recipe_id>[0-9]+)/$',
        views.api.api_vote, name='api_vote'),
    url(r'^api/recipes/(?P<recipe_id>[0-9]+)/$',
        views.api.api_recipes, name='api_recipes'),
    url(r'^api/ingredients/(?P<ingredient_id>[0-9]+)/$',
        views.api.api_ingredients, name='api_ingredients'),
    url(r'^api/terms$',
        views.api.api_terms, name='api_terms'),
    url(r'^api/food-groups/(?P<food_group_id>[0-9]+)/$',
        views.api.api_food_groups, name='api_food_groups'),
    url(r'^api/recipes/votes/(?P<recipe_id>[0-9]+)/$',
        views.api.api_votes, name='api_votes'),
    url(r'^om/$',
        views.site.about, name='about'),
    url(r'^bootstrap/$',
        views.site.bootstrap, name='bootstrap'),
    url(r'^media/(?P<path>.*)$',
        'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    ]
