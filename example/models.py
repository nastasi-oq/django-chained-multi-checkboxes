from django.db import models

TASTES = (
    (1, 'Salt'),
    (2, 'Sweet'),
    (3, 'Bitter'),
    (4, 'Sour'),
    (5, 'Umami'),
    (6, 'Fat'),
    (7, 'Ghost-taste'),
    (8, 'Virtual-taste')
)

class Ingredient(models.Model):
    class Meta:
        ordering = ['group']
    name = models.CharField(max_length=255 )
    group = models.IntegerField("Taste", choices=TASTES)
    is_visible = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name
    

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient)

    def __unicode__(self):
        return self.name
