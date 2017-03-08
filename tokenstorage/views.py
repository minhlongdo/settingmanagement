from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TokenStore
from .serializers import TokenStoreSerializer
from django.http import Http404, HttpResponseBadRequest, HttpResponseServerError
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND,\
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_202_ACCEPTED, HTTP_200_OK


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
            raise Exception

    def post(self, request):
        try:
            serializer = TokenStoreSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_201_CREATED)

            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        except Exception:
            raise HttpResponseServerError

    def put(self, request, instance_id, format=None):
        try:
            token = self.get_object(instance_id=instance_id)
            serializer = TokenStoreSerializer(token, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_202_ACCEPTED)

            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        except Http404:
            return Response(status=HTTP_404_NOT_FOUND)

        except Exception:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        """Returns github and slack tokens"""
        instance_id = request.GET.get('instance_id')

        token = self.get_object(instance_id=instance_id)
        serializer = TokenStoreSerializer(token)

        return Response(data=serializer.data, status=HTTP_200_OK)
