from typing import TYPE_CHECKING
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from follow.serializers import RequestWithUsernameSerializer


if TYPE_CHECKING:
    from django.http import HttpRequest


class RequestFollowAPIView(GenericAPIView):
    serializer_class = RequestWithUsernameSerializer

    def post(self, request: "HttpRequest"):
        return Response({"message": "started"})
