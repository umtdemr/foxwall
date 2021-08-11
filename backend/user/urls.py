from django.urls import path

from user.views.auth import views as v

app_name = "user"


urlpatterns = [
    path("register/", v.RegisterAPIView.as_view(), name="register"),
    path("login/", v.LoginAPIView.as_view(), name="login"),
    path("deneme/", v.DenemeBirAPIView.as_view(), name="deneme"),
]
