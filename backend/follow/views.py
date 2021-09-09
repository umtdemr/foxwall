from follow.models import FollowRequest
from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from user.serializers import RequestWithUsernameSerializer
from follow.serializers import (
    RequestReceivedFollowSerializer,
)
from follow.utils import (
    create_follow_request,
    delete_follow_request
)
from user.utils.follow_request import (
    allow_follow_request,
    unfollow
)


if TYPE_CHECKING:
    from django.http import HttpRequest


class RequestFollowAPIView(GenericAPIView):
    serializer_class = RequestWithUsernameSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request: "HttpRequest"):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        target_username = serializer.validated_data.get("username")

        User = get_user_model()
        creator = request.user
        target_user = User.get_user_with_username(target_username)

        create_follow_request(
            creator.id,
            target_user.id
        )

        return Response(
            {"message": "created"},
            status=status.HTTP_201_CREATED,
        )


class CancelRequestAPIView(GenericAPIView):
    serializer_class = RequestWithUsernameSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request: "HttpRequest"):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        target_username = serializer.validated_data.get(
            "username"
        )

        User = get_user_model()
        creator = request.user
        target = User.get_user_with_username(target_username)

        delete_follow_request(
            creator.id,
            target.id
        )

        return Response({
            "message": "deleted"
        })


class ReceivedFollowRequestsAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request: "HttpRequest"):
        received_requests = request.user.get_received_follow_requests()
        serializer = RequestReceivedFollowSerializer(
            instance=received_requests,
            many=True,
            context={'request': request}
        )
        return Response(
            {
                "results": serializer.data,
                "count": received_requests.count()
            }
        )


class RejectFollowRequestAPIView(GenericAPIView):
    serializer_class = RequestWithUsernameSerializer

    def post(self, request: "HttpRequest"):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        User = get_user_model()
        rejeting_username = serializer.validated_data.get("username")
        rejecting_user = User.get_user_with_username(rejeting_username)

        FollowRequest.delete_follow_request(
            creator_id=rejecting_user.id,
            target_user_id=request.user.id
        )

        return Response({
            "message": "rejected"
        })


class AllowFollowRequestAPIView(GenericAPIView):
    serializer_class = RequestWithUsernameSerializer

    def post(self, request: "HttpRequest"):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        User = get_user_model()
        allowing_username = serializer.validated_data.get("username")
        allowing_user = User.get_user_with_username(allowing_username)

        allow_follow_request(
            request.user.id,
            allowing_user.id
        )

        return Response(
            {
                "message": "allowed"
            }
        )


class UnfollowRequestAPIView(GenericAPIView):
    serializer_class = RequestWithUsernameSerializer

    def post(self, request: "HttpRequest"):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        User = get_user_model()
        unfollowing_username = serializer.validated_data.get("username")
        unfollowing_user = User.get_user_with_username(unfollowing_username)

        unfollow(
            request.user.id,
            unfollowing_user.id
        )

        return Response(
            {
                "message": "unfollowed"
            }
        )
