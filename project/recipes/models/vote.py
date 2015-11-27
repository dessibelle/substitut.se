# -*- coding: utf-8 -*-

""" Vote model. """

from django.db import connection, models, transaction
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _


def save_handler(sender, instance, **kwargs):
    instance.was_saved = True


class VoteManager(models.Manager):

    @staticmethod
    def get_ip_address(request):
        """Use requestobject to fetch client machine's IP Address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def get_user_agent(request):
        """Use requestobject to fetch client user agent."""
        return request.META.get('HTTP_USER_AGENT', '')

    def create_vote(self, request, recipe_id):
        """Create and saves a Vote."""
        if not request:
            raise ValueError('The given request must be set')

        if not recipe_id:
            raise ValueError('The given recipe id must be set')

        ip_address = VoteManager.get_ip_address(request)
        user_agent = VoteManager.get_user_agent(request)

        vote = self.model(recipe_id=recipe_id, ip_address=ip_address,
                          user_agent=user_agent, vote=+1)

        vote.save(using=self._db)

        if vote.was_saved:
            return vote
        else:
            raise Exception('Could not create vote for recipe {}, ip: {},\
                user_agent: {}'.format(recipe_id, ip_address, user_agent))

    def get_votes(self, recipe_id):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                count(*)
            FROM
                recipes_vote
            WHERE
                recipe_id = %s
            GROUP BY
                recipe_id""", [recipe_id])
        row = cursor.fetchone()
        try:
            return row[0]
        except:
            return 0


class Vote(models.Model):

    VOTE_UP = +1
    VOTE_DOWN = -1
    VOTE_CHOICES = (
        (VOTE_UP, _('Up')),
        (VOTE_DOWN, _('Down')),
    )

    class Meta:
        app_label = 'recipes'
        unique_together = [
            ["recipe", "created", "ip_address", "user_agent"],
        ]

    recipe = models.ForeignKey('Recipe', verbose_name=_('Recipe'))
    created = models.DateField(default=now, verbose_name=_('Created'))
    ip_address = models.GenericIPAddressField(verbose_name=_('IP Address'))
    user_agent = models.CharField(max_length=128, verbose_name=_('User Agent'))
    vote = models.SmallIntegerField(choices=VOTE_CHOICES, verbose_name=_('Vote'))

    objects = VoteManager()

    def __str__(self):
        return self.ip_address

    def __unicode__(self):
        return self.ip_address

    def is_upvote(self):
        return self.vote == self.VOTE_UP

    def is_downvote(self):
        return self.vote == self.VOTE_DOWN


def update_recipe_score(sender, instance, **kwargs):
    """ Updates the score for the recipe related to the given Vote. """
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE
            recipes_recipe
        SET
            score = (
                SELECT COALESCE(SUM(vote), 0) from recipes_vote
                WHERE recipes_vote.recipe_id = recipes_recipe.id
            )
        WHERE
            id = %%s""", [instance.recipe_id])
    transaction.commit_unless_managed()
    instance.was_saved = True

post_save.connect(update_recipe_score, sender=Vote)
