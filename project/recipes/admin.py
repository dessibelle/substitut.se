from django.contrib import admin
from reversion.admin import VersionAdmin
from recipes.models.term import Term
from recipes.models.food_group import FoodGroup
from recipes.models.ingredient import Ingredient
from recipes.models.recipe import Recipe, RecipeFoodGroup, RecipeIngredient
from recipes.models.unit import Unit, UnitIngredient
from recipes.models.vote import Vote
from sorl.thumbnail.admin import AdminImageMixin


class RecipeFoodGroupInline(admin.TabularInline):
    model = RecipeFoodGroup
    extra = 1
    classes = ('grp-collapse grp-open',)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    fields = ('ingredient', 'unit', 'amount', 'text', 'sort_order')
    raw_id_fields = ('ingredient',)
    # define the autocomplete_lookup_fields
    autocomplete_lookup_fields = {
        'm2m': ['ingredient'],
    }


class VoteAdmin(admin.ModelAdmin):
    list_display = ('recipe_id', 'ip_address', 'user_agent', 'created')
    list_filter = ['created']
    search_fields = ['recipe_id', 'ip_address']


class RecipeAdmin(AdminImageMixin, VersionAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'description']}),
        (None, {'fields': ['servings', 'instructions', 'image', 'status', 'lookup']}),
    ]
    inlines = [RecipeIngredientInline, RecipeFoodGroupInline]
    list_display = ('name', 'pub_date', 'status')
    list_filter = ['pub_date']
    search_fields = ['name']


class UnitIngredientInline(admin.TabularInline):
    model = UnitIngredient


class IngredientAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Data',
            {'fields': [
                'energy_kj',
                'energy_kcal',
                'protein', 'fat',
                'carbohydrates',
                'fibers',
                'salt',
                'water',
                'saturates',
                'monounsaturated',
                'trans_fat',
                'cholesterol',
                'vitamin_d',
                'vitamin_e',
                'vitamin_k',
                'vitamin_c',
                'vitamin_b6',
                'vitamin_b12',
                'iron'
            ], 'classes': ('grp-collapse grp-closed',)}),
    ]
    inlines = [UnitIngredientInline]
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(FoodGroup)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Unit)
admin.site.register(RecipeIngredient)
admin.site.register(Term)
admin.site.register(Vote, VoteAdmin)
