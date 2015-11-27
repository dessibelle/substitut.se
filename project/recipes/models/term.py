# -*- coding: utf-8 -*-

""" Term model. """

from django.db import models
from django.utils.translation import ugettext as _


class TermManager(models.Manager):

    def lookup(self, term):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                id,
                type,
                name,
                endpoint
            FROM
                recipes_term
            WHERE
                lower(name) LIKE %s
            ORDER BY
                name""", ["%%{}%%".format(term.lower())])
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
        verbose_name = _('Term')

    RECIPE = 0
    INGREDIENT = 1
    TAG = 2
    STATUS_CHOICES = (
        (RECIPE, 'Recipe'),
        (INGREDIENT, 'Ingredient'),
        (TAG, 'Tag'),
    )
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    type = models.SmallIntegerField(choices=STATUS_CHOICES, verbose_name=_('Type'))
    endpoint = models.CharField(max_length=255, verbose_name=_('Endpoint URL'))
    objects = TermManager()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
