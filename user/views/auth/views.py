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
from user.utils.generate import (
    generate_user_avatar,
    generate_user_cover,
    generate_username
)
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    ResetPasswordRequestSerializer,
    VerifyPasswordSerailizer
)

if TYPE_CHECKING:
    from collections import OrderedDict
    from rest_framework.request import Request


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
    def post(self, request: "Request", *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.on_valid(serializer.data)

    def on_valid(self, data: "OrderedDict"):
        username = data.get('username', '')
        email = data.get('email', '')
        password = data.get('password', '')

        auth_with_email = False
        if email:
            auth_with_email = True
        elif username and not auth_with_email:
            user = User.get_user_with_username(username)
            if user:
                email = user.email
        user = auth.authenticate(email=email, password=password)

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

    def post(self, request: "Request", *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return self.on_valid(serializer.validated_data)

    def on_valid(self, data: "OrderedDict"):
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        avatar = data.get("avatar")
        name = data.get("name")

        if not username:
            username = generate_username(email)
        if not avatar:
            avatar = generate_user_avatar()

        User = get_user_model()
        created_user = User.objects.create_user(
            email=email,
            password=password,
            username=username,
            is_email_verified=True,
        )
        UserProfile.objects.create(
            user=created_user,
            avatar=avatar,
            name=name,
            cover=generate_user_cover()
        )

        return Response(
            {
                "created": True,
                "username": created_user.username,
            },
            status=status.HTTP_201_CREATED,
        )


class RequestNewPasswordAPIView(GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request: "Request"):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        user = User.objects.get(email=email)

        token = user.request_password_token()

        return Response(
            {
                "sent": True,
                "token": token  # this should be not in here...
            }
        )


class VerifyNewPasswordAPIView(GenericAPIView):
    serializer_class = VerifyPasswordSerailizer

    def post(self, request: "Request"):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data.get("token")
        new_password = serializer.validated_data.get("new_password")

        User = get_user_model()
        user_obj = User.get_user_from_token(token)
        changed = user_obj.change_password(
            new_password
        )

        return Response(
            {
                "message": "password updated" if changed else "not updated"
            }
        )
