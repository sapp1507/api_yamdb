import datetime as dt

from django.core.exceptions import ValidationError
from django.db import models


class SlugBase(models.Model):
    """Абстрактная модель"""
    class Meta:
        abstract = True

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(SlugBase):
    pass


class Category(SlugBase):
    pass


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(max_length=4)
    description = models.CharField(max_length=256, blank=True)
    genre = models.ManyToManyField(Genre,
                                   related_name='titles',
                                   on_delete=models.SET_NULL)
    category = models.ForeignKey(Category,
                                 related_name='titles',
                                 on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def clean(self):
        if self.year > dt.datetime.now().year:
            raise ValidationError('Год выпуска не может быть больше текущего')
