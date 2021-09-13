from post.utils.crud import create_post
from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from .serializers import PostCreateSerializer, PostImageSerializer

if TYPE_CHECKING:
    from django.http import HttpRequest


class PostCreateAPIView(GenericAPIView):
    parser_classes = (
        MultiPartParser,
        FormParser,
    )
    permission_classes = (IsAuthenticated, )
    serializer_class = PostCreateSerializer

    def post(self, request: "HttpRequest"):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        images = dict((request.data).lists()).get("image")
        image_list = []
        if images:
            mod_data = []
            for image in images:
                mod_data.append({"image": image})
            image_serializer = PostImageSerializer(
                data=mod_data,
                many=True
            )

            image_serializer.is_valid(raise_exception=True)
            image_list = image_serializer.validated_data

        uuid = create_post(
            request.user,
            serializer.validated_data.get("text"),
            images=image_list
        )
        return Response(
            {"message": "created", "token": uuid},
            status=status.HTTP_201_CREATED
        )


class PostDeleteAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def delete(self, request: "HttpRequest", post_token: str):
        return Response({"message": "deleted"})
