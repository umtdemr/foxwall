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
        "recieved-requests/",
        v.RecievedFollowRequestsAPIView.as_view(),
        name="recieved-requests",
    ),
    path(

        "reject-follow-request/",
        v.RejectFollowRequestAPIView.as_view(),
        name="reject-follow-request",
    ),

]
