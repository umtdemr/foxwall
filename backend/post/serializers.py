from django.conf import settings

from rest_framework import serializers

from .models import Post
from core.serializer_fields import RestrictedImageFileSizeField


class PostImageSerializer(serializers.Serializer):
    image = RestrictedImageFileSizeField(
        max_upload_size=settings.MAX_PROFILE_AVATAR_SIZE,
        allow_empty_file=False,
        required=False
    )


class PostCreateSerializer(serializers.ModelSerializer):
    image = PostImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = (
            "text",
            "image",
        )
