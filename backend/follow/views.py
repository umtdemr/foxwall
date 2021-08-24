from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from follow.serializers import (
    RequestReceivedFollowSerializer,
    RequestWithUsernameSerializer
)
from follow.utils import (
    create_follow_request,
    delete_follow_request
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


class RecievedFollowRequestsAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request: "HttpRequest"):
        received_requests = request.user.get_received_follow_requests()
        serializer = RequestReceivedFollowSerializer(
            data=received_requests,
            many=True,
            context={'request': request}
        )
        serializer.is_valid()
        return Response(
            {
                "results": serializer.data,
                "count": received_requests.count()
            }
        )
