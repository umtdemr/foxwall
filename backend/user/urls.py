from django.urls import path

from user.views.auth.views import (
    RegisterAPIView,
    LoginAPIView,
    RequestNewPasswordAPIView,
    VerifyNewPasswordAPIView,
)
from user.views.authenticated.views import ProfileAPIView
from user.views.follow.views import FollowersAPIView, FollowsAPIView
from user.views.users.views import GetUserAPIView, GetUserPostsAPIView

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
    path("profile/<str:username>/", GetUserAPIView.as_view(), name="profile"),
    path(
        "profile/<str:username>/posts/",
        GetUserPostsAPIView.as_view(),
        name="profile-posts"
    ),
]
