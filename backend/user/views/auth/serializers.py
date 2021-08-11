from django.conf import settings
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from core.serializer_fields import RestrictedImageFileSizeField


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    username = serializers.CharField(allow_blank=True)
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.MAX_USERNAME_LENGTH,
        validators=[],
        required=False,
        allow_blank=True
    )
    password = serializers.CharField(
        min_length=settings.MIN_PASSWORD_LENGTH,
        max_length=settings.MAX_PASSWORD_LENGTH,
        validators=[validate_password],
    )
    name = serializers.CharField(
        max_length=settings.MAX_PROFILE_NAME_LENGTH
    )
    avatar = RestrictedImageFileSizeField(
        max_upload_size=settings.MAX_PROFILE_AVATAR_SIZE
    )
    email = serializers.EmailField(validators=[email_not_taken_validator])
    token = serializers.CharField()
