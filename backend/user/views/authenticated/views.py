from rest_framework.views import APIView
from rest_framework.response import Response


class UpdateUserAPIView(APIView):
    def patch(self, request):
        print(request.data)
        print(request.user)

        return Response({"q": "sdsadad"})
