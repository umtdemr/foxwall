from typing import TYPE_CHECKING

from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from user.models import User
from user.serializers import RequestWithUsernameSerializer, GetUserSerializer
from post.models import Post
from post.serializers import PostRetrieveSerializer


if TYPE_CHECKING:
    from django.http import HttpRequest


class GetUserAPIView(APIView):

    def get(self, request: "HttpRequest", username: str):
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


class GetUserPostsAPIView(APIView):

    def get(self, request: "HttpRequest", username: str):
        username_validation_serializer = RequestWithUsernameSerializer(
            data={"username": username}
        )
        username_validation_serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=username)
        posts = Post.active.get_user_posts(user.id)

        post_serializer = PostRetrieveSerializer(
            instance=posts,
            many=True
        )

        return Response(post_serializer.data)
