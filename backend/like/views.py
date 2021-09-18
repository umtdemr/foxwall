from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView

from like.utils.crud import toggle_like_on_post
from post.serializers import PostActionSerializer
from post.utils.crud import get_post


if TYPE_CHECKING:
    from django.http import HttpRequest


class LikeActionAPIView(GenericAPIView):
    serializer_class = PostActionSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request: "HttpRequest"):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = get_post(serializer.validated_data.get("uuid"))
        toggle_like_on_post(post, request.user)

        return Response(
            {
                "message": "created"
            }
        )
