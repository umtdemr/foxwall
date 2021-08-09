from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    username = serializers.CharField(allow_blank=True)
    password = serializers.CharField()
