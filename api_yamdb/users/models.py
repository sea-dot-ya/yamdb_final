from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    ROLES = [
        (ADMIN, "Administrator"),
        (MODERATOR, "Moderator"),
        (USER, "User"),
    ]

    bio = models.TextField(
        max_length=500,
        blank=True,
    )
    email = models.EmailField(blank=False, unique=True)
    role = models.CharField(choices=ROLES, max_length=10, default=USER)
    confirmation_code = models.CharField(max_length=256)

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN
