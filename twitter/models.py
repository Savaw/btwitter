from django.db import models
from django.conf import settings
from django.utils import timezone


class Tweet(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=140)
    parent_tweet = models.ForeignKey('Tweet', on_delete=models.PROTECT, blank=True, null=True)
    published_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.save()

    def __str__(self):
        return self.content

