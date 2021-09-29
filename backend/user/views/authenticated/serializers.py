from django.conf import settings

from rest_framework import serializers

from core.serializer_fields import RestrictedImageFileSizeField
from core.validators import (
    username_special_character_validator,
    name_not_contain_k_validator
)


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(
        allow_blank=True,
        required=False,
    )
    email = serializers.EmailField()
    name = serializers.CharField(
        allow_blank=True,
        required=False,
    )
    bio = serializers.CharField(
        allow_blank=True,
        required=False,
    )
    avatar = RestrictedImageFileSizeField(
        max_upload_size=settings.MAX_PROFILE_AVATAR_SIZE,
        allow_empty_file=True,
        required=False,
        allow_null=True,
    )
    cover = RestrictedImageFileSizeField(
        max_upload_size=settings.MAX_PROFILE_COVER_SIZE,
        allow_empty_file=True,
        required=False,
        allow_null=True
    )
    is_hidden = serializers.BooleanField()
    is_celebrity = serializers.BooleanField()


class UserProfileUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.MAX_USERNAME_LENGTH,
        required=False,
        allow_blank=True,
        validators=[
            username_special_character_validator
        ]
    )
    bio = serializers.CharField(
        allow_blank=True,
        required=False,
    )
    avatar = RestrictedImageFileSizeField(
        max_upload_size=settings.MAX_PROFILE_AVATAR_SIZE,
        allow_empty_file=True,
        required=False,
        allow_null=True,
    )
    cover = RestrictedImageFileSizeField(
        max_upload_size=settings.MAX_PROFILE_COVER_SIZE,
        allow_empty_file=True,
        required=False,
        allow_null=True
    )
    is_hidden = serializers.BooleanField(
        required=False
    )
    name = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=settings.MAX_PROFILE_NAME_LENGTH,
        validators=[name_not_contain_k_validator]
    )
