from django.contrib.auth.models import AbstractUser

from django.db import models

CHOICES = (
    ("user", "user"),
    ("admin", "admin"),
    ("moderator", "moderator"),
)


class User(AbstractUser):
    password = models.CharField(max_length=128, blank=True)
    bio = models.TextField("Биография", blank=True)
    role = models.CharField(max_length=12, choices=CHOICES, default="user")
    email = models.EmailField(db_index=True, unique=True)

    class Meta:
        ordering = ["id"]
