from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TokenStore
from .serializers import TokenStoreSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND,\
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_202_ACCEPTED, HTTP_200_OK, HTTP_204_NO_CONTENT
from .exceptions import Http400

import logging


class TokenStorageViewSet(viewsets.ViewSet):
    def list(self, request):
        logging.info('Retrieving everything')
        queryset = TokenStore.objects.all()
        serializer = TokenStoreSerializer(queryset, many=True)

        return Response(serializer.data, status=HTTP_200_OK)


class TokenStorage(APIView):
    """
    Retrieve and update TokenStore instance based on the query parameters instance_id and user_email.
    """

    def get_object(self, instance_id, user_email):
        try:
            if instance_id is None or len(instance_id.strip()) <= 0:
                logging.error('Trying to retrieve token based on empty instance_id={}'.format(instance_id))
                raise Http400
            if user_email is None or len(user_email.strip()) <= 0:
                logging.error('Trying to retrieve token based on empty email={}'.format(user_email))
                raise Http400

            logging.info('instance_id={} - user_email={}'.format(instance_id, user_email))

            return TokenStore.objects.get(instance_id=instance_id, user_email=user_email)

        except Http400:
            raise Http400

        except TokenStore.DoesNotExist:
            raise Http404

        except Exception:
            raise Exception

    def post(self, request):
        """
        Create or modify current entry of the token of a user.
        """
        try:
            logging.info('Incoming data={}'.format(request.data))
            token = self.get_object(request.data['instance_id'], request.data['user_email'])
            if token is not None:
                # Modify data only
                serializer = TokenStoreSerializer(token, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    logging.info('Modified data successfully')
                    return Response(serializer.data, status=HTTP_202_ACCEPTED)
                logging.info('Invalid data for modifying data')
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
            else:
                raise Http404

        except Http400:
            return Response(status=HTTP_400_BAD_REQUEST)

        except Http404:
            logging.info("Create new token entry")
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

    def get(self, request):
        """
        Returns all the token of the user based on the query parameters instance_id and user_email.
        """
        instance_id = request.GET.get('instance_id')
        user_email = request.GET.get('user_email')

        try:

            token = self.get_object(instance_id=instance_id, user_email=user_email)
            serializer = TokenStoreSerializer(token)

            logging.info('Retrieved data={}'.format(serializer.data))

            return Response(data=serializer.data, status=HTTP_200_OK)

        except Http404 as e:
            logging.warn(e)
            return Response(status=HTTP_404_NOT_FOUND)

        except Exception as e:
            logging.error(e)
            return Response(data=e, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        """
        Delete token entry based on instance_id and user_email in the request's body.
        """
        instance_id = request.data['instance_id']
        user_email = request.data['user_email']
        logging.info('Delete instance_id={} with user_email={}'.format(instance_id, user_email))
        token = self.get_object(instance_id=instance_id, user_email=user_email)
        token.delete()

        return Response(status=HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def clear_database(request):
    TokenStore.objects.all().delete()

    return Response(data='Clear database', status=HTTP_200_OK)
