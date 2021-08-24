from rest_framework import serializers

from user.models import User, UserProfile


class DisplayProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = (
            'avatar',
            'name',
            'is_hidden',
        )


class DisplayUserSerializer(serializers.ModelSerializer):
    profile = DisplayProfileSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'profile',
        )
        read_only_fields = ('id', )
