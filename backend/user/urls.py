from django.urls import path

from user.views.auth.views import LoginAPIView

app_name = "user"


urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login")
]
