from django.conf import settings
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.serializer_fields import RestrictedImageFileSizeField
from core.validators import (
    username_not_taken_validator,
    name_not_contain_k_validator,
    username_special_character_validator,
)
from user.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    username = serializers.CharField(allow_blank=True)
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.MAX_USERNAME_LENGTH,
        required=False,
        allow_blank=True,
        validators=[
            username_not_taken_validator,
            username_special_character_validator
        ]
    )
    password = serializers.CharField(
        min_length=settings.MIN_PASSWORD_LENGTH,
        max_length=settings.MAX_PASSWORD_LENGTH,
        validators=[validate_password],
    )
    name = serializers.CharField(
        max_length=settings.MAX_PROFILE_NAME_LENGTH,
        validators=[name_not_contain_k_validator]
    )
    avatar = RestrictedImageFileSizeField(
        max_upload_size=settings.MAX_PROFILE_AVATAR_SIZE,
        allow_empty_file=True,
        required=False
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(User.objects.all())
        ]
    )
