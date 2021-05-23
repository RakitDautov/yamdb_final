from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = "user", "user"
        MODERATOR = "moderator", "moderator"
        ADMIN = "admin", "admin"

    role = models.TextField(choices=Role.choices, default=Role.USER)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    confirmation_code = models.CharField(max_length=255)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        app_label = "users"
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-id"]

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR
