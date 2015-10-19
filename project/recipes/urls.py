from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',
        views.index, name='index'),
    url(r'^recept/(?P<lookup>[a-zA-Z0-9]+)(?:/(?P<slug>[a-zA-Z0-9-]+))?$',
        views.recipes, name='recipes'),
    url(r'^kategori/(?P<lookup>[a-zA-Z0-9]+)(?:/(?P<slug>[a-zA-Z0-9-]+))?$',
        views.food_groups, name='food_groups'),
    url(r'^ingrediens/(?P<lookup>[a-zA-Z0-9]+)(?:/(?P<slug>[a-zA-Z0-9-]+))?$',
        views.ingredients, name='ingredients'),
    url(r'^api/recipes/vote/(?P<recipe_id>[0-9]+)/$',
        views.api_vote, name='api_vote'),
    url(r'^api/recipes/(?P<recipe_id>[0-9]+)/$',
        views.api_recipes, name='api_recipes'),
    url(r'^api/ingredients/(?P<ingredient_id>[0-9]+)/$',
        views.api_ingredients, name='api_ingredients'),
    url(r'^api/terms$',
        views.api_terms, name='api_terms'),
    url(r'^api/food-groups/(?P<food_group_id>[0-9]+)/$',
        views.api_food_groups, name='api_food_groups'),
    url(r'^api/recipes/votes/(?P<recipe_id>[0-9]+)/$',
        views.api_votes, name='api_votes'),
    ]
