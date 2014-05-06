from django import forms
from django.forms import ModelForm
from django.forms.models import ChoiceField, ModelChoiceIterator
from example2.models import Ingredient, Recipe, TASTES

from chained_multi_checkboxes.forms import ModelChainedMultipleChoiceField
from chained_multi_checkboxes.widgets import ChainedCheckboxSelectMultiple

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        # fields is required to impose the correct visualization order
        fields = ('name', 'group', 'ingredients')

    group = ChoiceField(choices=TASTES)

    ingredients = ModelChainedMultipleChoiceField(parent_field='group', queryset=Ingredient.objects.all(), required=False)

