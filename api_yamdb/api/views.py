from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilterSet
from .mixins import ListCreateDestroyViewSet
from .permissions import (AdminOrReadOnly, AdminPermission,
                          ReviewCommentPermissions)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegisterSerializer,
                          ReviewSerializer, TitleSaveSerializer,
                          TitleSerializer, TokenSerializer, UserMeSerializer,
                          UserSerializer)
from .utils import send_confirmation_code

User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewCommentPermissions]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id'),
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id'),
        )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ReviewCommentPermissions]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
        serializer.save(author=self.request.user, review=review)


class GenreViewSet(ListCreateDestroyViewSet):
    permission_classes = [AdminOrReadOnly, ]
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name']
    lookup_field = 'slug'


class CategoryViewSet(ListCreateDestroyViewSet):
    permission_classes = [AdminOrReadOnly, ]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name']
    lookup_field = 'slug'


class TitleViewsSet(viewsets.ModelViewSet):
    """Вывод списка произведений с рейтингом."""
    permission_classes = [AdminOrReadOnly, ]
    filter_backends = [DjangoFilterBackend, ]
    filter_class = TitleFilterSet

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitleSaveSerializer

    def get_queryset(self):
        titles = Title.objects.annotate(
            rating=Avg('reviews__score')
        )
        return titles


class RegistrationAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        data = request.data
        username = data.get('username')
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(username=username)
        send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=request.data.get('username'))
        token = str(RefreshToken.for_user(user).access_token)
        data = {'acces': token}
        return Response(data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)
    lookup_field = 'username'


class UserMeAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserMeSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        serializer = self.serializer_class(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
