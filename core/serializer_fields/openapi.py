from rest_framework import serializers


class OpenAPIProfileSerializer(serializers.Serializer):
    name = serializers.CharField()
    avatar = serializers.CharField()
    cover = serializers.CharField()
    bio = serializers.CharField()
    is_hidden = serializers.BooleanField()
    is_celebrity = serializers.BooleanField()


class OpenAPIUserRetrieveSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    username = serializers.CharField()
    profile = OpenAPIProfileSerializer()
    is_following = serializers.BooleanField()
    is_followed_me = serializers.BooleanField()
    is_sent_follow_request = serializers.BooleanField()
    is_came_follow_request = serializers.BooleanField()
