import jwt

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import authentication, exceptions


class JWTAuthentication(authentication.BaseAuthentication):
    """ Custom JWT ``Authentication``"""

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)
        auth_data = auth_data.decode("utf-8")

        if not auth_data:
            return None

        auth_token = auth_data.split(" ")

        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed("Token is invalid")

        token = auth_token[1]
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms="HS256"
            )
            user = get_user_model().objects.get(
                username=payload['username']
            )
            return (user, token)

        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Your token is invalid")
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Your token is expired")
