from django.db import models
from django.db.utils import IntegrityError


class TokenStore(models.Model):
    instance_id = models.CharField(max_length=255, blank=False, auto_created=False)
    user_email = models.EmailField(primary_key=True, blank=False, auto_created=False, default='invalid@email.com')
    github_token = models.CharField(max_length=255, blank=True, null=False, default='')
    slack_token = models.CharField(max_length=255, blank=True, null=False, default='')
    vsts_token = models.CharField(max_length=255, blank=True, null=False, default='')
    slack_channel = models.CharField(max_length=255, blank=True, null=False, default='')

    class Meta:
        ordering = ('instance_id', 'user_email')
        unique_together = (('instance_id', 'user_email'),)

    def save(self, *args, **kwargs):
        if self.instance_id is None or len(self.instance_id) <= 0:
            raise IntegrityError("Instance ID cannot be None or empty")
        super(TokenStore, self).save(*args, **kwargs)
