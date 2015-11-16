from django.contrib.sitemaps import Sitemap
from recipes.models.recipe import Recipe


class RecipeSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Recipe.objects.filter(status=Recipe.PUBLISHED)

    def lastmod(self, obj):
        return obj.pub_date
