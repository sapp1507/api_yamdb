from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    bio = models.TextField('Биография', blank=True)
    role = models.CharField(max_length=12,
                            choices=settings.CHOICES,
                            default='user')
    email = models.EmailField(db_index=True, unique=True)

    class Meta:
        ordering = ['id']
