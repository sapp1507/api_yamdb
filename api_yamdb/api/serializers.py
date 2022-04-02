from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(title=title_id, author=user).exists():
            raise serializers.ValidationError(
                'Нельзя написать более одного отзыва на произведение'
            )
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
        model = Genre
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    def validate(self, attrs):
        slug = attrs['slug']
        if Genre.objects.filter(slug=slug).exists():
            raise serializers.ValidationError(
                f'slug: {slug} уже существует'
            )
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    def validate(self, attrs):
        slug = attrs['slug']
        if Category.objects.filter(slug=slug).exists():
            raise serializers.ValidationError(
                f'slug: {slug} уже существует'
            )
        return attrs


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = ['id', 'name', 'year', 'rating', 'description', 'genre',
                  'category']
        model = Title


class TitleSaveSerializer(TitleSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug', many=True,
                                         queryset=Genre.objects)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects)

    def validate(self, attrs):
        if 'year' in attrs and attrs['year'] > timezone.now().year:
            raise serializers.ValidationError(
                'Год не может быть больше текущего'
            )
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email')
        model = User

    def validate(self, data):
        username = data['username']
        if username == 'me':
            raise serializers.ValidationError(
                'Имя пользователя me недопустимо'
            )
        return super().validate(data)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=256)
    confirmation_code = serializers.CharField(max_length=512)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User

    def validate(self, data):
        if not data['username']:
            raise serializers.ValidationError(
                'Передайте имя пользователя'
            )
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = data['confirmation_code']
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                'Код подтверждения некорректный'
            )
        return super().validate(data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name',
        )
        model = User


class UserMeSerializer(UserSerializer):
    role = serializers.ChoiceField(choices=User.USER_ROLE_CHOICES,
                                   read_only=True)
