from rest_framework import serializers
from .models import TokenStore


class TokenStoreSerializer(serializers.Serializer):
    instance_id = serializers.CharField(read_only=True)
    github_token = serializers.CharField(read_only=False, allow_blank=True, allow_null=False)
    slack_token = serializers.CharField(read_only=False, allow_blank=True, allow_null=False)

    def update(self, instance, validated_data):
        instance.github_token = validated_data.get('github_token', instance.github_token)
        instance.slack_token = validated_data.get('slack_token', instance.slack_token)
        instance.save()

        return instance

    def create(self, validated_data):
        """
        Create and return a new `TokenStore` instance, given the validated data.
        """
        return TokenStore.objects.create(**validated_data)

