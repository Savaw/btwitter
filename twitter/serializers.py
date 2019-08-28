from rest_framework import serializers
from .models import Tweet
from django.utils import timezone


class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ['author', 'content', 'parent_tweet', 'published_date']
