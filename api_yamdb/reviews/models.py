from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from . import validators

User = get_user_model()


class SlugBase(models.Model):
    """Абстрактная модель"""
    class Meta:
        abstract = True

    name = models.CharField(max_length=256, verbose_name='Имя')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='slug')


class Genre(SlugBase):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(SlugBase):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    name = models.CharField(max_length=256, db_index=True,
                            verbose_name='Название')
    year = models.IntegerField(verbose_name='Год',
                               validators=[validators.year_validator])
    description = models.CharField(max_length=256, blank=True, null=True,
                                   verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='ID произведения',
    )
    text = models.TextField(
        'Текст отзыва',
        blank=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.IntegerField(
        'Оценка произведения',
        blank=False,
        validators=[
            MinValueValidator(
                1,
                message='Оценка должна быть от 1 до 10',
            ),
            MaxValueValidator(
                10,
                message='Оценка не может быть более 10',
            )
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            )
        ]
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='ID отзыва',
    )
    text = models.TextField(
        'Текст комментария',
        blank=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
