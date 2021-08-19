import jwt
import uuid
from datetime import datetime, timedelta
from typing import Optional

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
from core.validators import username_not_taken_validator
from user.utils import upload_to_user_directory


class UserManager(BaseUserManager):
    def create_user(self, email, password, username=None, **extra_fields):
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
            password,
            username,
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
                "email": self.email,
                "exp": datetime.utcnow() + timedelta(hours=24),
            },
            settings.JWT_SECRET_KEY,
            algorithm='HS256'
        )

    @classmethod
    def is_email_taken(cls, email: str) -> bool:
        try:
            cls.objects.get(email=email)
            return True
        except User.DoesNotExist:
            return False

    @classmethod
    def is_username_taken(cls, username: str) -> bool:
        try:
            cls.objects.get(username=username)
            return True
        except User.DoesNotExist:
            return False

    @classmethod
    def get_username_with_email(cls, email: str) -> str:
        try:
            user = cls.objects.get(email=email)
            return user.username
        except Exception:
            return ""

    def update(
        self,
        username: Optional[str] = None,
        name: Optional[str] = None,
        bio: Optional[str] = None,
        is_hidden: Optional[bool] = None,
        avatar=None,
        cover=None,

    ):
        if username:
            self._update_username(username)

        profile = self.profile
        if name:
            profile.name = name
        if bio:
            profile.bio = bio
        if is_hidden:
            profile.is_hidden = is_hidden
        if avatar:
            profile.avatar = avatar
        if cover:
            profile.cover = cover

        self.save()
        profile.save()

    def _update_username(self, username: str):
        if self.username == username:
            return

        username_not_taken_validator(username)

        self.username = username

    def get_profile(self) -> "UserProfile":
        return self.profile


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
        processors=[ResizeToFill(500, 500)],
        upload_to=upload_to_user_directory,
        max_length=1000,
    )
    cover = ProcessedImageField(
        blank=False,
        null=True,
        format="JPEG",
        options={"quality": 90},
        processors=[ResizeToFit(width=1024, upscale=False)],
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
