from django.urls import path

from user.views.auth.views import (
    RegisterAPIView,
    LoginAPIView,
    RequestNewPasswordAPIView,
    VerifyNewPasswordAPIView,
)
from user.views.authenticated.views import ProfileAPIView
from user.views.follow.views import FollowersAPIView, FollowsAPIView

app_name = "user"


urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path(
        "password-reset-request/",
        RequestNewPasswordAPIView.as_view(),
        name="password-reset-request",
    ),
    path(
        "reset-password/",
        VerifyNewPasswordAPIView.as_view(),
        name="reset-password",
    ),
    path("me/", ProfileAPIView.as_view(), name="update"),
    path("followers/", FollowersAPIView.as_view(), name="followers"),
    path("follows/", FollowsAPIView.as_view(), name="follows"),
]
