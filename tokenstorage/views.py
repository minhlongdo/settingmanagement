from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TokenStore
from .serializers import TokenStoreSerializer
from .responses import JSONResponse
from django.http import Http404, HttpResponseBadRequest, HttpResponseServerError
from rest_framework.status import HTTP_400_BAD_REQUEST


class TokenStorage(APIView):
    """
    Retrieve and update TokenStore instance
    """

    def get_object(self, instance_id):
        try:
            if instance_id is None or len(instance_id.strip()) <= 0:
                raise HttpResponseBadRequest

            return TokenStore.objects.get(instance_id=instance_id)
        except TokenStore.DoesNotExist:
            raise Http404

        except Exception:
            raise HttpResponseServerError

    def post(self, request):
        try:
            serializer = TokenStoreSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Exception:
            raise HttpResponseServerError

    def put(self, request, instance_id, format=None):
        try:
            token = self.get_object(instance_id=instance_id)
            serializer = TokenStoreSerializer(token, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Exception:
            raise HttpResponseServerError

    def get(self, request):
        """Returns github and slack tokens"""
        instance_id = request.GET.get('instance_id')

        token = self.get_object(instance_id=instance_id)
        serializer = TokenStoreSerializer(token)

        return JSONResponse(data=serializer.data)
