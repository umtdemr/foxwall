from typing import TYPE_CHECKING

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import PostCreateSerializer, PostImageSerializer

if TYPE_CHECKING:
    from django.http import HttpRequest


class PostCreateAPIView(GenericAPIView):
    parser_classes = (
        MultiPartParser,
        FormParser,
    )
    serializer_class = PostCreateSerializer
    #  TODO: Must add permission for auth.

    def post(self, request: "HttpRequest"):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        images = dict((request.data).lists())['image']
        if images:
            mod_data = []
            for image in images:
                mod_data.append({"image": image})
            image_serializer = PostImageSerializer(
                data=mod_data,
                many=True
            )

            image_serializer.is_valid(raise_exception=True)

        return Response({"message": "Started to post section!"})
