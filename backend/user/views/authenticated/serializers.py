from django.conf import settings

from rest_framework import serializers

from core.serializer_fields import RestrictedImageFileSizeField
from core.validators import (
    username_not_taken_validator,
    username_special_character_validator,
)


class UserProfileUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.MAX_USERNAME_LENGTH,
        required=False,
        allow_blank=True,
        validators=[
            username_not_taken_validator,
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
        required=False
    )
    cover = RestrictedImageFileSizeField(
        max_upload_size=settings.MAX_PROFILE_AVATAR_SIZE,
        allow_empty_file=True,
        required=False
    )
    is_hidden = serializers.BooleanField(
        required=False
    )
