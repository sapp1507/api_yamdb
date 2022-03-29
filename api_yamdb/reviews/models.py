from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    pass


class Review(models.Model):
    text = models.TextField(
        'Текст отзыва',
        blank=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
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
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField(
        'Текст комментария',
        blank=False,
    )
    author = models.ForeignKey(
        'Автор',
        User,
        on_delete=models.CASCADE,
        related_name='comments',
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
