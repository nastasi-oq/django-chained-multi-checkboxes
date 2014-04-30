from django.db import models

TASTES = (
    (1, 'Salt'),
    (2, 'Sweet'),
    (3, 'Bitter'),
    (4, 'Sour'),
    (5, 'Umami'),
    (6, 'Fat')
)

class Ingredient(models.Model):
    class Meta:
        ordering = ['taste']
    taste = models.IntegerField(choices=TASTES)
    name = models.CharField(max_length=255 )
    
    def __unicode__(self):
        return self.name
    

class Recipe(models.Model):
    name = models.CharField(max_length=255 )
    ingredients = models.ManyToManyField(Ingredient)

    def __unicode__(self):
        return self.name
