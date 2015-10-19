from django.core.management.base import BaseCommand, CommandError
from recipes.models.term import Term
from recipes.models.recipe import Recipe
from recipes.models.ingredient import Ingredient
from recipes.models.food_group import FoodGroup
from django.core.urlresolvers import reverse


class Command(BaseCommand):
    help = 'Index recipes, ingredients and tags'

    def handle(self, *args, **options):
        try:
            Term.objects.all().delete()
            # Index recipes
            recipe_count = 0
            recipes = Recipe.objects.get_index()
            for recipe in recipes:
                term = Term(name=recipe['name'],
                            type=Term.RECIPE,
                            endpoint=reverse('api_recipes', args=[recipe['id']]))
                term.save()
                recipe_count += 1
            self.stdout.write('Indexed {} recipes'.format(recipe_count))

            # Index ingredients
            ingredient_count = 0
            ingredients = Ingredient.objects.get_index()
            for ingredient in ingredients:
                term = Term(name=ingredient['name'],
                            type=Term.INGREDIENT,
                            endpoint=reverse('api_ingredients', args=[ingredient['id']]))
                term.save()
                ingredient_count += 1
            self.stdout.write('Indexed {} ingredients'.format(ingredient_count))

            # Index Food groups
            food_group_count = 0
            food_groups = FoodGroup.objects.get_index()
            for food_group in food_groups:
                term = Term(name=food_group['name'],
                            type=Term.TAG,
                            endpoint=reverse('api_food_groups', args=[food_group['id']]))
                term.save()
                food_group_count += 1
            self.stdout.write('Indexed {} food groups'.format(food_group_count))


        except Exception as e:
            raise CommandError('Indexing failed: {}'.format(e))
