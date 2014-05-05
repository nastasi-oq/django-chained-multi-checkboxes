from django.contrib import admin
from nested_inlines.admin import NestedModelAdmin, NestedStackedInline
from models import Library, Book, Ingredient, Recipe
from forms import RecipeForm

admin.site.register(Ingredient)

class RecipeInline(NestedStackedInline):
    model = Recipe
    form = RecipeForm
    extra = 1

class BookInline(NestedStackedInline):
    model = Book
    inlines = [RecipeInline,]
    extra = 1

class LibraryAdmin(NestedModelAdmin):
    model = Library
    inlines = [BookInline,]

admin.site.register(Library, LibraryAdmin)



