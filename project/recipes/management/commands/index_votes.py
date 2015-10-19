from django.core.management.base import BaseCommand, CommandError
from recipes.models.vote import Vote
from recipes.models.recipe import Recipe


class Command(BaseCommand):
    help = 'Index votes'

    def handle(self, *args, **options):
        try:
            votes = Vote.objects.get_index()
            for vote in votes:
                recipe = Recipe.objects.get(pk=vote['recipe_id'])
                recipe.num_votes = vote['num_votes']
                recipe.save()
                self.stdout.write('Indexed {} votes for recipe #{}'.format(vote['num_votes'], vote['recipe_id']))

        except Exception as e:
            raise CommandError('Indexing failed: {}'.format(e))
