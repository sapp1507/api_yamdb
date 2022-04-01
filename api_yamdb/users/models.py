from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

USER_ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
)


# Еще круто было бы добавить проперти(@property) для вычисления ролей.
# Тогда в коде можно будет просто вызывать их как методы, не сравнивая с
# константами и вся логика проверки будет сосредоточена в классе юзера.
class User(AbstractUser):

    bio = models.TextField('Биография', blank=True)
    role = models.CharField(max_length=12,
                            choices=USER_ROLE_CHOICES,
                            default=USER)
    email = models.EmailField(db_index=True, unique=True)

    class Meta:
        ordering = ['id']
