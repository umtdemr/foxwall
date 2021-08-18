from typing import TYPE_CHECKING

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiExample, extend_schema

from user.models import User, UserProfile
from .serializers import LoginSerializer, RegisterSerializer

if TYPE_CHECKING:
    from collections import OrderedDict


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    @extend_schema(
        description=_("User can authenticate with both username and email"),
        examples=[
            OpenApiExample(
                _("With Username"),
                value={
                    "username": "testusername",
                    "password": "password"
                },
                request_only=True,
            ),
            OpenApiExample(
                _("With Email"),
                value={
                    "email": "email@test.com",
                    "password": "password"
                },
                request_only=True,
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.on_valid(serializer.data)

    def on_valid(self, data: "OrderedDict"):
        username = data.get('username', '')
        email = data.get('email', '')
        password = data.get('password', '')

        authenticated_w_username = False
        if username:
            authenticated_w_username = True
        elif email and not authenticated_w_username:
            username = User.get_username_with_email(email)
        user = auth.authenticate(username=username, password=password)

        if user:
            auth_token = user.token
            data = {
                "username": user.username,
                "email": user.email,
                "token": auth_token
            }
            return Response(data, status.HTTP_200_OK)
        return Response({"detail": "invalid credentials"},
                        status.HTTP_401_UNAUTHORIZED)


class RegisterAPIView(GenericAPIView):
    parser_classes = (
        MultiPartParser,
        FormParser,
    )
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return self.on_valid(serializer.validated_data)

    def on_valid(self, data: "OrderedDict"):
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        avatar = data.get("avatar")
        name = data.get("name")

        User = get_user_model()
        created_user = User.objects.create_user(
            email=email,
            password=password,
            username=username,
            is_email_verified=True,
        )
        UserProfile.objects.create(user=created_user, avatar=avatar, name=name)

        return Response(
            {
                "created": True,
                "username": created_user.username,
            },
            status=status.HTTP_201_CREATED,
        )
