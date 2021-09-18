from django.conf import settings

from rest_framework import serializers

from .models import Post
from core.serializer_fields import RestrictedImageFileSizeField
from core.validators.post import post_exist_validator


class PostImageSerializer(serializers.Serializer):
    image = RestrictedImageFileSizeField(
        max_upload_size=settings.MAX_PROFILE_AVATAR_SIZE,
        allow_empty_file=False,
        required=False
    )


class PostCreateSerializer(serializers.ModelSerializer):
    image = PostImageSerializer(many=True, required=False)
    text = serializers.CharField(max_length=300, required=False)

    class Meta:
        model = Post
        fields = (
            "text",
            "image",
        )


class PostActionSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(
        validators=[post_exist_validator]
    )
