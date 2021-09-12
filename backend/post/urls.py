from django.urls import path

from . import views

app_name = "post"


urlpatterns = [
    path(
        "create/",
        views.PostCreateAPIView.as_view(),
        name="create"
    )
]
