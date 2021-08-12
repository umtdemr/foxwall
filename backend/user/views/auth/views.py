from typing import TYPE_CHECKING

from django.contrib import auth
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from user.models import UserProfile
from .serializers import LoginSerializer, RegisterSerializer


if TYPE_CHECKING:
    from collections import OrderedDict


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user:
            auth_token = user.token
            serializer = self.serializer_class(user)
            data = {
                "user": serializer.data,
                "token": auth_token
            }
            return Response(data, status.HTTP_200_OK)
        return Response(
            {"detail": "invalid credentials"}, status.HTTP_401_UNAUTHORIZED
        )


class DenemeBirAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "detail": "You can see it cuz you are authenticated"
            }
        )


class RegisterAPIView(GenericAPIView):
    parser_classes = (MultiPartParser, FormParser,)
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
        created_user = User.objects.create(
            email=email,
            username=username,
            password=password,
            is_email_verified=True
        )
        UserProfile.objects.create(
            user=created_user,
            avatar=avatar,
            name=name
        )

        return Response(
            {
                "created": True,
                "username": created_user.username,
            },
            status=status.HTTP_201_CREATED
        )
