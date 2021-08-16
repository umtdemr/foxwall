from typing import TYPE_CHECKING

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import UserProfileUpdateSerializer

if TYPE_CHECKING:
    from django.http.request import QueryDict
    from user.models import User
    from django.http.request import HttpRequest


class UpdateUserAPIView(GenericAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = (IsAuthenticated, )

    def patch(self, request: "HttpRequest"):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)

        return self.on_valid(serializer.data, request.user)

    def on_valid(self, data: "QueryDict", user: "User"):

        user.update(
            username=data.get("username"),
            name=data.get("name"),
            bio=data.get("bio"),
            is_hidden=data.get("is_hidden"),
            avatar=data.get("avatar"),
            cover=data.get("cover"),
        )

        return Response({"updated": True})
