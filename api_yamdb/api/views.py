from django.db import models
from rest_framework import viewsets
from reviews.models import Title, Genre, Category

from .serializers import TitleSerializer, GenreSerializer, CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class TitleViewsSet(viewsets.ModelViewSet):
    """Вывод списка произведений с рейтингом."""
    serializer_class = TitleSerializer

    def get_queryset(self):
        titles = Title.objects.all().annotate(
            rating=models.Sum(models.F('reviews__score')) / models.Count(
                models.F('reviews'))
        )
        return titles
