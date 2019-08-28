from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Tweet
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from .models import Tweet
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import TweetForm
from .serializers import TweetSerializer
from rest_framework import status


@api_view(['GET', 'POST'])
def tweet_list(request):
    if request.method == 'GET':
        tweets = Tweet.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = TweetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['published_date'] = timezone.now()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_404_NOT_FOUND)


def new_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                tweet = form.save(commit=False)
                tweet.author = request.user
                tweet.published_date = timezone.now()
                tweet.save()
                return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'twitter/new_tweet.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            # messages.success(request, f"new account created: {username}")
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserCreationForm()
    return render(request, 'twitter/signup.html', {'form': form})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                # messages.success(request, f"You are logged in as {username}")
                return redirect('tweet_list')
        else:
            pass
            # messages.error(request, "invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'twitter/login.html', {'form': form})
    pass


def logout_request(request):
    logout(request)
    return redirect('tweet_list')

