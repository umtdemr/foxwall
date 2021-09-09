from follow.models import Follow
from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from follow.serializers import FollowSerailizer


if TYPE_CHECKING:
    from django.http import HttpRequest


class FollowersAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: "HttpRequest"):
        search_param = request.query_params.get("q")

        followers = request.user.get_followers(q=search_param)
        serializer = FollowSerailizer(
            instance=followers,
            many=True,
        )

        return Response({
            "results": serializer.data,
            "count": followers.count()
        })
