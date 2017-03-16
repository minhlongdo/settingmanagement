from rest_framework import serializers
from .models import TokenStore


class TokenStoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = TokenStore
        fields = ('instance_id', 'user_email', 'github_token', 'github_user',
                  'github_org', 'slack_token', 'vsts_token', 'slack_channel')
