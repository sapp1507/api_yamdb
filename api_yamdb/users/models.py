from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
)


class User(AbstractUser):

    bio = models.TextField('Биография', blank=True)
    role = models.CharField(max_length=12,
                            choices=USER_ROLE_CHOICES,
                            default='user')
    email = models.EmailField(db_index=True, unique=True)

    class Meta:
        ordering = ['id']
