from rest_framework import serializers
from .models import TokenStore


class TokenStoreSerializer(serializers.Serializer):
    instance_id = serializers.CharField(read_only=True)
    github_token = serializers.CharField(read_only=False, allow_blank=True, allow_null=False)
    slack_token = serializers.CharField(read_only=False, allow_blank=True, allow_null=False)

    def update(self, instance, validated_data):
        instance.github_token = validated_data.get('github_token', instance.github_token)
        return TokenStore.objects.update(validated_data)

    def create(self, validated_data):
        pass

