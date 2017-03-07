from django.db import models
from django.db.utils import IntegrityError


class TokenStore(models.Model):
    instance_id = models.CharField(primary_key=True, max_length=255, blank=False, auto_created=False)
    github_token = models.CharField(max_length=255, blank=True, null=False)
    slack_token = models.CharField(max_length=255, blank=True, null=False)

    class Meta:
        ordering = ('instance_id',)

    def save(self, *args, **kwargs):
        if self.instance_id is None or len(self.instance_id) <= 0:
            raise IntegrityError("Instance ID cannot be None or empty")
        super(TokenStore, self).save(*args, **kwargs)
