from django.db import models

class Library(models.Model):
    name = models.CharField("name", max_length=255)

    def __unicode__(self):
        return self.name

class Book(models.Model):
    a = models.ForeignKey(Library)
    name = models.CharField("name", max_length=255)

    def __unicode__(self):
        return self.name

TASTES = (
    ('', '--------'),
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
    book = models.ForeignKey(Book)
    name = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient)

    def __unicode__(self):
        return self.name
