from django.urls import path

from . import views as v

app_name = "follow"


urlpatterns = [
    path(
        "request/",
        v.RequestFollowAPIView.as_view(),
        name="request",
    ),
    path(
        "cancel-request/",
        v.CancelRequestAPIView.as_view(),
        name="cancel-request",
    ),
    path(
        "received-requests/",
        v.ReceivedFollowRequestsAPIView.as_view(),
        name="received-requests",
    ),
    path(

        "reject-follow-request/",
        v.RejectFollowRequestAPIView.as_view(),
        name="reject-follow-request",
    ),
    path(

        "allow-follow-request/",
        v.AllowFollowRequestAPIView.as_view(),
        name="allow-follow-request",
    ),
    path(
        "unfollow/",
        v.UnfollowRequestAPIView.as_view(),
        name="unfollow",
    ),
]
