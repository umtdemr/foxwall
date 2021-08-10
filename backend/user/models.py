
import jwt
import uuid

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.conf import settings

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeToFill

from core.abstract_models import TimeInfoModel
from user.utils import upload_to_user_directory


class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email or not username:
            raise ValueError("Users must have email")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        user.set_password(password)
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
    sec_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "username"

    @property
    def token(self):
        return jwt.encode(
            {
                "username": self.username,
                "email": self.email
            },
            settings.JWT_SECRET_KEY
        )


class UserProfile(TimeInfoModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    name = models.CharField(max_length=200)
    avatar = ProcessedImageField(
        blank=False,
        null=True,
        format="JPEG",
        options={"quality": 90},
        processors=[ResizeToFit(width=1024, upscale=False)],
        upload_to=upload_to_user_directory,
        max_length=1000,
    )
    cover = ProcessedImageField(
        blank=False,
        null=True,
        format="JPEG",
        options={"quality": 90},
        processors=[ResizeToFill(500, 500)],
        upload_to=upload_to_user_directory,
        max_length=1000,
    )
    bio = models.TextField(blank=True, null=True)
    is_celebrity = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)

    class Meta:
        index_together = [("id", "user")]

    def __repr__(self) -> str:  # pragma: no cover
        return "<UserProfile %s>" % self.user.username

    def __str__(self) -> str:
        return self.user.username
