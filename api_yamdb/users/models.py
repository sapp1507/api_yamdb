from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    )

    bio = models.TextField('Биография', blank=True)
    role = models.CharField(max_length=12,
                            choices=USER_ROLE_CHOICES,
                            default=USER)
    email = models.EmailField(db_index=True, unique=True)

    class Meta:
        ordering = ['id']
