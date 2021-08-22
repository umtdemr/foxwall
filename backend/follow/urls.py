from django.urls import path

from . import views as v

app_name = "follow"


urlpatterns = [
    path(
        "request/",
        v.RequestFollowAPIView.as_view(),
        name="request",
    )
]
