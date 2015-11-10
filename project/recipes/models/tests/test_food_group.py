# -*- coding: utf-8 -*-
from django.test import TestCase
from recipes.models.food_group import FoodGroup
from recipes.models.recipe import Recipe, RecipeFoodGroup


class FoodGroupTestCase(TestCase):
    def setUp(self):
        fg_1 = FoodGroup.objects.create(name="Test Food Group 1")
        fg_2 = FoodGroup.objects.create(name="Test Food Group 2")
        re_1 = Recipe.objects.create(
            name="Test Recipe 1",
            description="Test description 1",
            instructions="Test instructions 1",
            num_votes=5,
            status=1)
        re_2 = Recipe.objects.create(
            name="Test Recipe 2",
            description="Test description 2",
            instructions="Test instructions 2",
            num_votes=9,
            status=1)
        re_3 = Recipe.objects.create(
            name="Test Recipe 3",
            description="Test description 3",
            instructions="Test instructions 3",
            num_votes=15,
            status=1)

        self.lookup_1 = fg_1.lookup
        self.lookup_2 = fg_2.lookup

        RecipeFoodGroup.objects.create(recipe=re_1, food_group=fg_1)
        RecipeFoodGroup.objects.create(recipe=re_2, food_group=fg_1)
        RecipeFoodGroup.objects.create(recipe=re_3, food_group=fg_2)

    def test_popular_categories(self):
        """Check that the category with the most votes comes first."""
        pop = FoodGroup.objects.get_top()
        try:
            fg = pop[0]
            self.assertEqual(fg["name"], "Test Food Group 2")
        except IndexError:
            self.fail("No popular food groups found.")

    def test_get_index(self):
        """Check index."""
        index = FoodGroup.objects.get_index()
        try:
            self.assertEqual(len(index), 2)
            self.assertEqual(index[0]["name"], "Test Food Group 1")
        except IndexError:
            self.fail("No food groups found.")

    def test_get_slug(self):
        """Check slug."""
        slug = FoodGroup.objects.get_slug(self.lookup_1)
        self.assertEqual(slug['slug'], "test-food-group-1")

