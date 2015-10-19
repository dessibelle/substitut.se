from PIL import Image
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string


class RecipeManager(models.Manager):
    def lookup(self, term):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, name FROM recipes_recipe
            WHERE name LIKE ?
            ORDER BY name""", ["%%{}%%".format(term)])
        result_list = []
        for row in cursor.fetchall():
            result_list.append({
                'id': row[0],
                'name': row[1]
            })
        return result_list

    def get_index(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, name FROM recipes_recipe WHERE status = ?",
            [Recipe.PUBLISHED]
        )
        result_list = []
        for row in cursor.fetchall():
            result_list.append({
                'id': row[0],
                'name': row[1]
            })
        return result_list

    def get_slug(self, lookup):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, name
            FROM recipes_recipe
            WHERE lookup = ?
            AND status = ?""", [lookup, Recipe.PUBLISHED])

        result = cursor.fetchone()
        try:
            return {
                'id': result[0],
                'slug': slugify(result[1])
            }
        except:
            return {}


class Recipe(models.Model):
    UNPUBLISHED = 0
    PUBLISHED = 1
    STATUS_CHOICES = (
        (UNPUBLISHED, 'Unpublished'),
        (PUBLISHED, 'Published'),
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='static/recipes/images/', blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES)
    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient')
    servings = models.SmallIntegerField(default=4)
    objects = RecipeManager()
    num_votes = models.IntegerField(default=0)
    lookup = models.SlugField(
        unique=True,
        default=get_random_string,
        max_length=13,
    )

    class Meta:
        app_label = 'recipes'

    @models.permalink
    def get_absolute_url(self):
        return ("recipes", [self.lookup, self.slug()])

    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def save(self, size=(600, 600), *args, **kwargs):
        super(Recipe, self).save(*args, **kwargs)
        if not self.id or not self.image:
            return
        pw = self.image.width
        ph = self.image.height
        nw = size[0]
        nh = size[1]

        if (pw, ph) != (nw, nh):
            filename = str(self.image.path)
            image = Image.open(filename)
            pr = float(pw) / float(ph)
            nr = float(nw) / float(nh)

            if pr > nr:
                # image aspect is wider than destination ratio
                tw = int(round(nh * pr))
                image = image.resize((tw, nh), Image.ANTIALIAS)
                l = int(round((tw - nw) / 2.0))
                image = image.crop((l, 0, l + nw, nh))
            elif pr < nr:
                # image aspect is taller than destination ratio
                th = int(round(nw / pr))
                image = image.resize((nw, th), Image.ANTIALIAS)
                t = int(round((th - nh) / 2.0))
                print((0, t, nw, t + nh))
                image = image.crop((0, t, nw, t + nh))
            else:
                # image aspect matches the destination ratio
                image = image.resize(size, Image.ANTIALIAS)

            image.save(filename)


class RecipeFoodGroup(models.Model):
    recipe = models.ForeignKey(Recipe)
    food_group = models.ForeignKey('FoodGroup')

    class Meta:
        app_label = 'recipes'


class RecipeIngredient(models.Model):
    unit = models.ForeignKey('Unit')
    ingredient = models.ForeignKey('Ingredient')
    recipe = models.ForeignKey(Recipe)
    amount = models.FloatField()
    text = models.CharField(max_length=255)

    class Meta:
        app_label = 'recipes'
