from typing import TYPE_CHECKING

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import PostCreateSerializer


if TYPE_CHECKING:
    from django.http import HttpRequest


class PostCreateAPIView(GenericAPIView):
    serializer_class = PostCreateSerializer

    def post(self, request: "HttpRequest"):
        return Response({"message": "Started to post section!"})
