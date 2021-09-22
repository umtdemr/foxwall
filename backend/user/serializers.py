from django.conf import settings

from rest_framework import serializers

from user.models import User, UserProfile
from core.validators import (
    user_username_exists,
    username_special_character_validator
)


class DisplayProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = (
            'avatar',
            'name',
            'is_hidden',
            'is_celebrity',
        )


class DisplayUserSerializer(serializers.ModelSerializer):
    profile = DisplayProfileSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'profile',
        )
        read_only_fields = ('id', )


class RequestWithUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.MAX_USERNAME_LENGTH,
        allow_blank=False,
        validators=[
            username_special_character_validator,
            user_username_exists
        ]
    )
