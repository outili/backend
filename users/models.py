from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """Creates and saves a User with the given email"""
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    is_student = models.BooleanField(default=True)
    is_instructor = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password", "first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email
