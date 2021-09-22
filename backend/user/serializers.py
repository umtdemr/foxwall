from django.conf import settings

from rest_framework import serializers

from user.models import User, UserProfile
from core.validators import (
    user_username_exists,
    username_special_character_validator
)
from core.serializer_fields.user import (
    IsFollowingField
)


class DisplayProfileSerializer(serializers.ModelSerializer):
    """
        Profile serializer for just getting `summary` about profile\n
        Working with DisplayUserSerializer
    """

    class Meta:
        model = UserProfile
        fields = (
            "avatar",
            "name",
            "is_hidden",
            "is_celebrity",
        )


class DisplayUserSerializer(serializers.ModelSerializer):
    """
        User serializer for just getting `summary` about user
    """

    profile = DisplayProfileSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "profile",
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


class GetProfileSerializer(serializers.ModelSerializer):
    """
        Profile serializer for getting full info for profile.
    """

    class Meta:
        model = UserProfile
        fields = (
            "name",
            "avatar",
            "cover",
            "bio",
            "is_hidden",
            "is_celebrity",
        )


class GetUserSerializer(serializers.ModelSerializer):
    """
        User serializer for getting full info about user.
    """

    profile = GetProfileSerializer()
    is_following = IsFollowingField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "profile",
            "is_following",
        )
