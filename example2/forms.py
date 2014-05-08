from django import forms
from django.forms import ModelForm
from django.forms.models import ChoiceField
from example2.models import Ingredient, Recipe, TASTES

from chained_multi_checkboxes.forms import ModelChainedMultipleChoiceField

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        # fields is required to impose the correct visualization order
        fields = ('name', 'form_taste', 'ingredients')

    form_taste = ChoiceField(choices=TASTES)

    ingredients = ModelChainedMultipleChoiceField(parent_field='form_taste', order_fields=('taste', 'name'), queryset=Ingredient.objects.all(), required=False)

