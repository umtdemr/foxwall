from django.urls import path

from user.views.auth.views import (
    RegisterAPIView,
    LoginAPIView,
    RequestNewPasswordAPIView
)
from user.views.authenticated.views import (
    ProfileAPIView
)

app_name = "user"


urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path(
        "password-reset-request/",
        RequestNewPasswordAPIView.as_view(),
        name="password-reset-request"
    ),
    path("me/", ProfileAPIView.as_view(), name="update"),
]
