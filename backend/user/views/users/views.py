from typing import TYPE_CHECKING

from rest_framework.views import APIView
from rest_framework.response import Response


if TYPE_CHECKING:
    from django.http import HttpRequest


class GetUserAPIView(APIView):

    def get(self, request: "HttpRequest", username: str):
        print(request)
        print(username)

        return Response({"message": "Started!"})
