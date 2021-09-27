from typing import TYPE_CHECKING

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from follow.serializers import FollowerSerailizer, FollowSerailizer


if TYPE_CHECKING:
    from django.http import HttpRequest


class FollowersAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=None,
        responses=FollowerSerailizer
    )
    def get(self, request: "HttpRequest"):
        search_param = request.query_params.get("q")

        followers = request.user.get_followers(q=search_param)
        serializer = FollowerSerailizer(
            instance=followers,
            many=True,
        )

        return Response({
            "results": serializer.data,
            "count": followers.count()
        })


class FollowsAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=None,
        responses=FollowSerailizer
    )
    def get(self, request: "HttpRequest"):
        search_param = request.query_params.get("q")

        follows = request.user.get_follows(q=search_param)
        serializer = FollowSerailizer(
            instance=follows,
            many=True,
        )

        return Response({
            "results": serializer.data,
            "count": follows.count()
        })
