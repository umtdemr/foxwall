from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeToFill

from core.abstract_models import TimeInfoModel


class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have email")
        if not username:
            # Add an helper to automatically create username
            pass
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email,
            username,
            password,
            is_staff=True,
            is_superuser=True,
        )
        return user


class User(AbstractBaseUser, PermissionsMixin, TimeInfoModel):
    """Custom user model"""

    username = models.CharField(max_length=35, unique=True)
    email = models.EmailField(unique=True)
    first_name = None
    last_name = None

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "username"


# class UserProfile(TimeInfoModel):
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name="profile",
#     )
#     name = models.CharField(max_length=200)
#     avatar =
#     bio = models.TextField(blank=True, null=True)
#     is_celebrity = models.BooleanField(default=False)
#     is_hidden = models.BooleanField(default=False)
