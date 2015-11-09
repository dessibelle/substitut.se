from django.db import models
# from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from recipe import Recipe


class FoodGroupManager(models.Manager):

    """Foodgroup manager."""

    def get_top(self):
        """Return popular categories."""
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT fg.id, fg.name, SUM(r.num_votes) as num
            FROM recipes_foodgroup fg
            INNER JOIN recipes_recipefoodgroup rfg ON rfg.food_group_id = fg.id
            INNER JOIN recipes_recipe r ON rfg.recipe_id = r.id
            WHERE r.status = %s
            GROUP BY fg.id
            ORDER BY num DESC""", [Recipe.PUBLISHED])
        result_list = []
        for row in cursor.fetchall():
            result_list.append({
                'id': row[0],
                'name': row[1]
            })
        return result_list

    def get_latest(self):
        """Return categories with newest recipes."""
        pass

    def get_food_groups(self, recipe_id=None):
        """Return food groups for a single recipe."""
        from django.db import connection
        cursor = connection.cursor()
        if recipe_id is not None:
            cursor.execute("""
                SELECT fg.id, fg.name, fg.lookup
                FROM recipes_foodgroup fg
                INNER JOIN recipes_recipefoodgroup rfg ON rfg.food_group_id = fg.id
                INNER JOIN recipes_recipe r ON rfg.recipe_id = r.id
                WHERE r.id = %s""", [recipe_id])
        else:
            cursor.execute("""
                SELECT fg.id, fg.name, fg.lookup
                FROM recipes_foodgroup fg
                ORDER BY fg.name""")

        result_list = []
        for row in cursor.fetchall():
            fg = FoodGroup(id=row[0], name=row[1], lookup=row[2])
            result_list.append({
                'id': row[0],
                'name': row[1],
                'url': fg.get_absolute_url()
            })
        return result_list

    def get_index(self):
        """Return data used for tag indexing."""
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT fg.id, fg.name
            FROM recipes_foodgroup fg
            INNER JOIN recipes_recipefoodgroup rfg ON rfg.food_group_id = fg.id
            INNER JOIN recipes_recipe r ON rfg.recipe_id = r.id
            WHERE r.status = %s
            GROUP BY fg.id""", [Recipe.PUBLISHED])
        result_list = []
        for row in cursor.fetchall():
            result_list.append({
                'id': row[0],
                'name': row[1]
            })
        return result_list

    def get_slug(self, lookup):
        """Return slug for the given hash."""
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, name
            FROM recipes_foodgroup
            WHERE lookup = %s""", [lookup])

        result = cursor.fetchone()
        try:
            return {
                'id': result[0],
                'slug': slugify(result[1])
            }
        except:
            return {}


class FoodGroup(models.Model):
    name = models.CharField(max_length=200)
    recipes = models.ManyToManyField(Recipe, through='RecipeFoodGroup')
    objects = FoodGroupManager()
    lookup = models.SlugField(
        unique=True,
        default=get_random_string,
        max_length=13,
    )

    class Meta:
        app_label = 'recipes'

    @models.permalink
    def get_absolute_url(self):
        return ("food_groups", [self.lookup, self.slug()])

    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
