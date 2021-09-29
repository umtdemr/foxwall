from django.urls import path

from . import views


app_name = "like"


urlpatterns = [
    path("action/", views.LikeActionAPIView.as_view(), name="action"),
]
