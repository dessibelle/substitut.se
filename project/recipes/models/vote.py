from django.db import models
from django.utils.timezone import now
from django.db.models.signals import post_save


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
                          user_agent=user_agent)

        vote.save(using=self._db)

        if vote.was_saved:
            return vote
        else:
            raise Exception('Could not create vote for recipe {}, ip: {},\
                user_agent: {}'.format(recipe_id, ip_address, user_agent))

    def get_index(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT recipe_id, count(*)
            FROM recipes_vote
            GROUP BY recipe_id""")
        rows = cursor.fetchall()
        ret = []
        for row in rows:
            ret.append({'recipe_id': row[0], 'num_votes': row[1]})
        return ret

    def get_votes(self, recipe_id):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT count(*)
            FROM recipes_vote
            WHERE recipe_id = ?
            GROUP BY recipe_id""", [recipe_id])
        row = cursor.fetchone()
        try:
            return row[0]
        except:
            return 0


class Vote(models.Model):

    class Meta:
        app_label = 'recipes'
        unique_together = [
            ["recipe", "created", "ip_address", "user_agent"],
        ]

    recipe = models.ForeignKey('Recipe')
    created = models.DateField(default=now)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=128)
    objects = VoteManager()

    def __str__(self):
        return self.ip_address

    def __unicode__(self):
        return self.ip_address

post_save.connect(save_handler, sender=Vote)
