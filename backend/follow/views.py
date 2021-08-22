from follow.models import FollowRequest
from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from follow.serializers import RequestWithUsernameSerializer


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

        follow_req = FollowRequest.create_follow_request(
            creator_id=creator.id,
            target_user_id=target_user.id
        )
        print(follow_req, creator, target_user)

        return Response({"message": "started"})
