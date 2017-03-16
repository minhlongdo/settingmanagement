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
        self.vsts_token = 'vsts_token'
        self.slack_channel = 'slack_channel'
        self.user_email = 'user@email.com'

    def tearDown(self):
        TokenStore.objects.all().delete()

    def test_create_token_store_with_none_id_expect_integrity_exception(self):
        self.assertRaises(IntegrityError,
                          TokenStore.objects.create,
                          instance_id=None,
                          github_token=self.github_token,
                          slack_token=self.slack_token,
                          vsts_token=self.vsts_token,
                          slack_channel=self.slack_channel,
                          user_email=self.user_email)

    def test_create_token_store_with_empty_id_expect_integrity_exception(self):
        self.assertRaises(IntegrityError,
                          TokenStore.objects.create,
                          instance_id='',
                          github_token=self.github_token,
                          slack_token=self.slack_token,
                          vsts_token=self.vsts_token,
                          slack_channel=self.slack_channel,
                          user_email=self.user_email)

    def test_create_token_store_with_id_expect_pass(self):
        TokenStore.objects.create(instance_id=self.instance_id,
                                  github_token=self.github_token,
                                  slack_token=self.slack_token,
                                  vsts_token=self.vsts_token,
                                  slack_channel=self.slack_channel,
                                  user_email=self.user_email)

        token_store = TokenStore.objects.get(instance_id=self.instance_id)

        self.assertEquals(token_store.instance_id, self.instance_id)
        self.assertEquals(token_store.github_token, self.github_token)
        self.assertEquals(token_store.slack_token, self.slack_token)
        self.assertEquals(token_store.vsts_token, self.vsts_token)
        self.assertEquals(token_store.user_email, self.user_email)


class TokenStoreViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.view = TokenStorage.as_view()
        self.base_url = '/v1/tokenstorage/'
        self.valid_data = {
            'instance_id': 'test-instance-id',
            'github_token': 'test-github-token',
            'slack_token': 'test-slack-token',
            'vsts_token': 'test-vsts-token',
            'slack_channel': 'test-slack-channel',
            'user_email': 'user@email.com',
            'github_user': 'github-user',
            'github_org': 'github_org'
        }
        self.invalid_data = {
            'instance_id': '',
            'github_token': 'test-github-token',
            'slack_token': 'test-slack-token',
            'slack_channel': 'slack_channel',
            'vsts_token': 'test-vsts-token',
            'user_email': 'user@email.com'
        }

    def test_post_valid_data(self):
        request = self.factory.post(self.base_url, data=self.valid_data, format='json')
        response = self.view(request)

        self.assertEquals(response.status_code, 201, "Expects status code 201")
        self.assertEquals(response.data, self.valid_data, "Expects the same data")

    def test_post_empty_instance_id_data(self):
        request = self.factory.post(self.base_url, data=self.invalid_data, format='json')
        response = self.view(request)

        self.assertEquals(response.status_code, 400, "Expects status code 200")

    def test_post_none_instance_id_data(self):
        request = self.factory.post(self.base_url, data=self.invalid_data, format='json')
        response = self.view(request)

        self.assertEquals(response.status_code, 400, "Expects status code 200")

    def test_post_modify_data(self):
        TokenStore.objects.create(instance_id=self.valid_data['instance_id'],
                                  user_email=self.valid_data['user_email'],
                                  github_token=self.valid_data['github_token'],
                                  slack_token=self.valid_data['slack_token'],
                                  slack_channel=self.valid_data['slack_channel'],
                                  vsts_token=self.valid_data['vsts_token'],
                                  github_user=self.valid_data['github_user'],
                                  github_org=self.valid_data['github_org'])
        modified_data = {
            "instance_id": self.valid_data['instance_id'],
            "user_email": self.valid_data['user_email'],
            "github_token": "modified_github_token",
            "slack_token": "modified_slack_token",
            "vsts_token": "modified_slack_token",
            "slack_channel": "modified_slack_channel",
            "github_org": "modified_github_org",
            "github_user": "modified_github_user"
        }
        request = self.factory.post(self.base_url, data=modified_data)
        response = self.view(request)

        self.assertEquals(response.data, modified_data)
        self.assertEquals(response.status_code, 202, "Expects status code 202")

    def test_get_non_existing_instance_id(self):

        request = self.factory.get(
            self.base_url+"?instance_id={}&user_email={}".format(self.valid_data['instance_id'],
                                                                 self.valid_data['user_email']))
        response = self.view(request)

        self.assertEquals(response.status_code, 404)

    def test_get_existing_instance_id(self):
        TokenStore.objects.create(instance_id=self.valid_data['instance_id'],
                                  github_token=self.valid_data['github_token'],
                                  slack_token=self.valid_data['slack_token'],
                                  vsts_token=self.valid_data['vsts_token'],
                                  slack_channel=self.valid_data['slack_channel'],
                                  user_email=self.valid_data['user_email'],
                                  github_user=self.valid_data['github_user'],
                                  github_org=self.valid_data['github_org'])

        request = self.factory.get(
            self.base_url+"?instance_id={}&user_email={}".format(self.valid_data['instance_id'],
                                                                 self.valid_data['user_email']))
        response = self.view(request)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, self.valid_data)
