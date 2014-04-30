from django.contrib import admin
from models import Ingredient, Recipe
from forms import RecipeForm

admin.site.register(Ingredient)

class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    form = RecipeForm


admin.site.register(Recipe, RecipeAdmin)

