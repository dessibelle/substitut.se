from django.core.management.base import BaseCommand
from recipes.models import Unit, Ingredient, UnitIngredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        Unit.objects.all().delete()
        Ingredient.objects.all().delete()
