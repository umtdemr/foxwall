from django.urls import path

from . import views

app_name = "post"


urlpatterns = [
    path(
        "create/",
        views.PostCreateAPIView.as_view(),
        name="create"
    ),
    path(
        "delete/<uuid:post_token>/",
        views.PostDeleteAPIView.as_view(),
        name="delete"
    ),
    path(
        "timeline/",
        views.PostTimelineAPIView.as_view(),
        name="timeline"
    ),
]
