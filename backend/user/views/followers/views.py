from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


if TYPE_CHECKING:
    from django.http import HttpRequest


class FollowersAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: "HttpRequest"):
        user = request.user
        search_param = request.GET.get("q")

        followers = user.get_followers(q=search_param)
        print(followers)

        return Response({"message": "Yes Dude"})
