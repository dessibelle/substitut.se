from django.db import models


class TermManager(models.Manager):

    def lookup(self, term):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, type, name, endpoint FROM recipes_term
            WHERE name LIKE %s
            ORDER BY name""", ["%%{}%%".format(term)])
        result_list = []
        for row in cursor.fetchall():
            result_list.append({
                'id': row[0],
                'type': row[1],
                'name': row[2],
                'endpoint': row[3]
            })
        return result_list


class Term(models.Model):

    class Meta:
        app_label = 'recipes'

    RECIPE = 0
    INGREDIENT = 1
    TAG = 2
    STATUS_CHOICES = (
        (RECIPE, 'Recipe'),
        (INGREDIENT, 'Ingredient'),
        (TAG, 'Tag'),
    )
    name = models.CharField(max_length=128)
    type = models.SmallIntegerField(choices=STATUS_CHOICES)
    endpoint = models.CharField(max_length=255)
    objects = TermManager()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
