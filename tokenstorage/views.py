from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TokenStore
from .serializers import TokenStoreSerializer
from django.http import Http404, HttpResponseBadRequest
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND,\
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_202_ACCEPTED, HTTP_200_OK

import logging


class TokenStorage(APIView):
    """
    Retrieve and update TokenStore instance
    """

    def get_object(self, instance_id, user_email):
        try:
            if instance_id is None or len(instance_id.strip()) <= 0:
                logging.error('Trying to retrieve token based on empty instance_id={}'.format(instance_id))
                raise HttpResponseBadRequest
            if user_email is None or len(user_email.strip()) <= 0:
                logging.error('Trying to retrieve token based on empty email={}'.format(user_email))
                raise HttpResponseBadRequest

            logging.info('instance_id={} - user_email={}'.format(instance_id, user_email))

            return TokenStore.objects.get(instance_id=instance_id, user_email=user_email)

        except TokenStore.DoesNotExist:
            raise Http404

        except Exception:
            raise Exception

    def post(self, request):
        try:
            logging.info('Incoming data={}'.format(request.data))
            serializer = TokenStoreSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                logging.info('Successfully create new token entry')
                return Response(serializer.data, status=HTTP_201_CREATED)

            logging.error("Invalid data=", serializer.errors)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            logging.error(e)
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, instance_id, format=None):
        try:
            logging.info('Modifying token entry')
            user_email = request.data['user_email']
            token = self.get_object(instance_id=instance_id, user_email=user_email)
            serializer = TokenStoreSerializer(token, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logging.info('Modified data successfully')
                return Response(serializer.data, status=HTTP_202_ACCEPTED)
            logging.info('Invalid data for modifying data')
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        except Http404:
            logging.warn('Could not find entry to modify')
            return Response(status=HTTP_404_NOT_FOUND)

        except Exception as e:
            logging.error(e)
            return Response(e, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        """Returns github and slack tokens"""
        instance_id = request.GET.get('instance_id')
        user_email = request.GET.get('user_email')

        token = self.get_object(instance_id=instance_id, user_email=user_email)
        serializer = TokenStoreSerializer(token)

        logging.info('Retrieved data={}'.format(serializer.data))

        return Response(data=serializer.data, status=HTTP_200_OK)
