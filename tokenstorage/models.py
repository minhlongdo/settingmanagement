from django.db import models


class TokenStore(models.Model):
    instance_id = models.CharField(primary_key=True, max_length=255, null=False, blank=False)
    github_token = models.CharField(max_length=255, blank=True, null=False)
    slack_token = models.CharField(max_length=255, blank=True, null=False)

    class Meta:
        ordering = ('instance_id',)
