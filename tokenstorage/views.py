from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TokenStore
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR,\
    HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST


class TokenStorage(APIView):

    def post(self, request):
        try:
            data = request.DATA
            return Response(status=HTTP_201_CREATED)
        except Exception:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            data = request.DATA
            return Response(status=HTTP_200_OK)
        except Exception:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        """Returns github and slack tokens"""
        instance_id = request.GET.get('instance_id')

        if instance_id is None or len(instance_id.strip()) <= 0:
            return Response(status=HTTP_400_BAD_REQUEST)

        try:
            return Response(status=HTTP_200_OK)
        except Exception:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)