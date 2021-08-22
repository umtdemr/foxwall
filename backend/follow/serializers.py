from django.conf import settings

from rest_framework import serializers

from core.validators import (
    username_special_character_validator,
    user_username_exists,
)


class RequestWithUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.MAX_USERNAME_LENGTH,
        validators=[
            username_special_character_validator,
            user_username_exists
        ]
    )
