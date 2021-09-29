from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from user.models import User
from user.serializers import RequestWithUsernameSerializer, GetUserSerializer
from user.utils.search import search_user
from post.models import Post
from post.serializers import PostRetrieveSerializer
from core.serializer_fields.openapi import OpenAPIUserRetrieveSerializer
from core.validators.views import required_query_param
from core.pagination import PostPagination


if TYPE_CHECKING:
    from rest_framework.request import Request


class GetUserAPIView(APIView):

    @extend_schema(
        request=None,
        responses=OpenAPIUserRetrieveSerializer
    )
    def get(self, request: "Request", username: str):
        username_validation_serializer = RequestWithUsernameSerializer(
            data={"username": username}
        )
        username_validation_serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=username)

        user_serializer = GetUserSerializer(
            instance=user,
            context={"request": request}
        )

        return Response(user_serializer.data)


class GetUserPostsAPIView(ListAPIView):
    pagination_class = PostPagination
    serializer_class = PostRetrieveSerializer

    def get_queryset(self):
        username = self.kwargs.get("username")
        return Post.active.get_user_posts_with_username(username)

    def list(self, request, *args, **kwargs):
        username = kwargs.get("username")
        username_validation_serializer = RequestWithUsernameSerializer(
            data={"username": username}
        )
        username_validation_serializer.is_valid(raise_exception=True)
        return super().list(request, *args, **kwargs)


class SearchUserAPIView(APIView):

    def get(self, request: "Request"):
        required_query_param(
            "q",
            request
        )

        q = request.query_params.get("q")
        search_list, count = search_user(q)

        if count == 0:
            return Response(
                {"message": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = GetUserSerializer(
            instance=search_list,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)
