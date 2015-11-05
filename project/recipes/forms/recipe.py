from django.forms import ModelForm
from recipes.models.recipe import Recipe
from django.utils.translation import ugettext_lazy as _


class RecipeForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['instructions'].widget.attrs.update({'class': 'form-control'})
        self.fields['servings'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Recipe
        fields = ['name', 'description', 'instructions', 'servings']
        labels = {
            'name': _('Name'),
        }
        help_texts = {
            'name': _('Some useful help text.'),
        }
        error_messages = {
            'name': {
                'max_length': _("This recipe's name is too long."),
            },
        }
