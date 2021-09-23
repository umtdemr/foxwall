import jwt
import uuid
from datetime import datetime, timedelta
from typing import Optional, Union, TYPE_CHECKING

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.conf import settings

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeToFill
from rest_framework import exceptions

from user import JwtTypes
from core.abstract_models import TimeInfoModel
from core.validators import username_not_taken_validator
from user.utils import upload_to_user_directory


if TYPE_CHECKING:
    from follow.models import Follow, FollowRequest


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
                "exp": datetime.utcnow() + timedelta(days=24),
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

    @classmethod
    def get_user_with_username(cls, username: str) -> Union["User", None]:
        try:
            user = cls.objects.get(username=username)
            return user
        except Exception:
            return None

    @classmethod
    def get_user_from_token(cls, token: str) -> Union["User", None]:
        try:
            decoded = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms="HS256"
            )
            if decoded.get("type") == JwtTypes.REQUEST_NEW_PASSWORD:
                return cls.objects.get(
                    id=decoded.get("user_id")
                )
        except jwt.DecodeError:
            raise exceptions.ValidationError("Token is invalid")
        except jwt.ExpiredSignatureError:
            raise exceptions.ValidationError("Token expired")
        except Exception:
            raise exceptions.ValidationError("Some error occurred")

    def change_password(self, password: str) -> bool:
        self.set_password(password)
        self.save()
        return True

    def request_password_token(self):
        generated_request_token = self._generate_password_request_token()
        #  send email...

        return generated_request_token

    def get_profile(self) -> "UserProfile":
        return self.profile

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

    def _generate_password_request_token(self):
        return jwt.encode(
            {
                "type": JwtTypes.REQUEST_NEW_PASSWORD,
                "user_id": self.id,
                "exp": datetime.utcnow() + timedelta(days=1)
            },
            settings.JWT_SECRET_KEY,
            algorithm='HS256'
        )

    def get_received_follow_requests(self) -> "FollowRequest":
        return self.coming_follow_requests.all()

    def get_followers(self, q: Optional[str] = None) -> "Follow":
        if q:
            return self.followers.filter(
                Q(user__email=q) |
                Q(user__username__icontains=q) |
                Q(user__profile__name__icontains=q)
            )
        return self.followers.all()

    def get_follows(self, q: Optional[str] = None) -> "Follow":
        if q:
            return self.follows.filter(
                Q(followed_user__email=q) |
                Q(followed_user__username__icontains=q) |
                Q(followed_user__profile__name__icontains=q)
            )
        return self.follows.all()

    def is_following_with_id(self, control_id: int) -> bool:
        return self.follows.filter(followed_user_id=control_id).exists()


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
