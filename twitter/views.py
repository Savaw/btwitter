from django.shortcuts import render
from .models import Tweet
from django.utils import timezone
# Create your views here.


def tweet_list(request):
    tweets = Tweet.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'twitter/tweet_list.html', {'tweets': tweets})
