from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    pass


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        'Оценка произведения',
        default=0,
        blank=True,
        validators=[
            MinValueValidator(
                0,
                message='Оценка не может быть отрицательной',
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
