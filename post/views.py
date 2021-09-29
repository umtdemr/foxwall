from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .serializers import (
    PostCreateSerializer,
    PostImageSerializer,
    PostRetrieveSerializer
)
from .permissions import PostIsOwner
from .utils.crud import create_post, get_post, get_timeline_posts
from core.serializer_fields import MessageSerializer
from core.pagination import PostPagination

if TYPE_CHECKING:
    from rest_framework.request import Request


class PostCreateAPIView(GenericAPIView):
    parser_classes = (
        MultiPartParser,
        FormParser,
    )
    permission_classes = (IsAuthenticated, )
    serializer_class = PostCreateSerializer

    def post(self, request: "Request"):
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
    permission_classes = (PostIsOwner, )

    @extend_schema(
        request=None,
        responses={204: MessageSerializer}
    )
    def delete(self, request: "Request", post_token: str):
        obj = get_post(post_token)
        self.check_object_permissions(request, obj)

        obj.delete()

        return Response(
            {"message": "deleted"},
            status=status.HTTP_204_NO_CONTENT
        )


class PostTimelineAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostRetrieveSerializer
    pagination_class = PostPagination

    def get_queryset(self):
        return get_timeline_posts(self.request.user)
