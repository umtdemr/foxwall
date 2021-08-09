from django.urls import path

from user.views.auth.views import LoginAPIView, DenemeBirAPIView

app_name = "user"


urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("deneme/", DenemeBirAPIView.as_view(), name="deneme"),
]
