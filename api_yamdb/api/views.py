from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Comment, Review, Title, Genre, Category

from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, ReviewSerializer,
                          TitleSerializer, GenreSerializer, CategorySerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Comment,
            id=review_id
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Comment,
            pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)


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
