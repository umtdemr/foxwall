from rest_framework import serializers

from user.serializers import DisplayUserSerializer
from follow.models import FollowRequest


class RequestReceivedFollowSerializer(serializers.ModelSerializer):
    creator = DisplayUserSerializer()

    class Meta:
        model = FollowRequest
        fields = (
            'id',
            'creator',
        )
        read_only_fields = ('id', )
