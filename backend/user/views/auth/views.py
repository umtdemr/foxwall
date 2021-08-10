import jwt

from django.contrib import auth
from django.conf import settings

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import LoginSerializer


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
