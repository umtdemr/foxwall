from typing import TYPE_CHECKING

from rest_framework.views import APIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .serializers import UserProfileUpdateSerializer, UserSerializer
from user.utils import get_user_data_with_serializer

if TYPE_CHECKING:
    from django.http.request import QueryDict
    from user.models import User
    from django.http.request import HttpRequest


class ProfileAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    parser_classes = (
        JSONParser,
        MultiPartParser,
        FormParser,
    )

    @extend_schema(
        request=UserSerializer
    )
    def get(self, request: "HttpRequest"):
        serializer = get_user_data_with_serializer(request.user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)

    @extend_schema(
        request=UserProfileUpdateSerializer,
    )
    def patch(self, request: "HttpRequest"):
        serializer = UserProfileUpdateSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        return self.on_valid(serializer.validated_data, request.user)

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
