from django.test import TestCase
from tokenstorage.models import TokenStore
from django.db.utils import IntegrityError
from rest_framework.test import APIRequestFactory, APITestCase
from .views import TokenStorage


class TokenStoreTestCase(TestCase):
    def setUp(self):
        self.instance_id = 'instance_id'
        self.github_token = 'github_token'
        self.slack_token = 'slack_token'

    def test_create_token_store_with_none_id_expect_integrity_exception(self):
        self.assertRaises(IntegrityError,
                          TokenStore.objects.create,
                          instance_id=None,
                          github_token=self.github_token,
                          slack_token=self.slack_token)

    def test_create_token_store_with_empty_id_expect_integrity_exception(self):
        self.assertRaises(IntegrityError,
                          TokenStore.objects.create,
                          instance_id='',
                          github_token=self.github_token,
                          slack_token=self.slack_token)

    def test_create_token_store_with_id_expect_pass(self):
        TokenStore.objects.create(instance_id=self.instance_id,
                                  github_token=self.github_token,
                                  slack_token=self.slack_token)

        token_store = TokenStore.objects.get(instance_id=self.instance_id)

        self.assertEquals(token_store.instance_id, self.instance_id)
        self.assertEquals(token_store.github_token, self.github_token)
        self.assertEquals(token_store.slack_token, self.slack_token)


class TokenStoreViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.view = TokenStorage.as_view()
        self.base_url = '/v1/tokenstorage/'

    def test_post_valid_data(self):
        valid_data = {
            'instance_id': 'test-instance-id',
            'github_token': 'test-github-token',
            'slack_token': 'test-slack-token'
        }
        request = self.factory.post(self.base_url, data=valid_data, format='json')
        response = self.view(request)

        self.assertEquals(response.status_code, 201, "Expects status code 201")
        self.assertEquals(response.data, valid_data, "Expects the same data")

    def test_post_empty_instance_id_data(self):
        invalid_data = {
            'instance_id': '',
            'github_token': 'test-github-token',
            'slack_token': 'test-slack-token'
        }

        request = self.factory.post(self.base_url, data=invalid_data, format='json')
        response = self.view(request)

        self.assertEquals(response.status_code, 400, "Expects status code 200")

    def test_post_none_instance_id_data(self):
        invalid_data = {
            'instance_id': None,
            'github_token': 'test-github-token',
            'slack_token': 'test-slack-token'
        }

        request = self.factory.post(self.base_url, data=invalid_data, format='json')
        response = self.view(request)

        self.assertEquals(response.status_code, 400, "Expects status code 200")

    def test_put_modify_data_exiting_instance_id(self):
        instance_id = "test_instance_id"
        valid_data = {
            'instance_id': instance_id,
            'github_token': 'test-github-token',
            'slack_token': 'test-slack-token'
        }

        TokenStore.objects.create(instance_id=instance_id, github_token='github_token', slack_token='slack_token')

        token = TokenStore.objects.get(instance_id=instance_id)

        self.assertEquals(token.instance_id, instance_id)
        self.assertEquals(token.github_token, 'github_token')
        self.assertEquals(token.slack_token, 'slack_token')

        request = self.factory.put(self.base_url + instance_id, data=valid_data, format='json')
        response = self.view(request, instance_id)

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data, valid_data)

    def test_put_modify_data_non_existing_instance_id(self):
        instance_id = "test_instance_id"
        valid_data = {
            'instance_id': instance_id,
            'github_token': 'test-github-token',
            'slack_token': 'test-slack-token'
        }

        request = self.factory.put(self.base_url + instance_id, data=valid_data, format='json')
        response = self.view(request, instance_id)

        self.assertEquals(response.status_code, 404)

    def test_put_modify_invalid_data_instance_id(self):
        instance_id = ''
        valid_data = {
            'instance_id': instance_id,
            'github_token': 'test-github-token',
            'slack_token': 'test-slack-token'
        }

        request = self.factory.put(self.base_url + instance_id, data=valid_data, format='json')
        response = self.view(request, instance_id)

        self.assertEquals(response.status_code, 500)
