from typing import TYPE_CHECKING

from rest_framework.views import APIView
from rest_framework.response import Response

from user.models import User
from user.serializers import RequestWithUsernameSerializer, GetUserSerializer


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

        return Response({"user": user_serializer.data})
