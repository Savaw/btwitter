from django.shortcuts import render, redirect
from .models import Tweet
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def tweet_list(request):
    tweets = Tweet.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'twitter/tweet_list.html', {'tweets': tweets})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            messages.success(request, f"new account created: {username}")
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
                messages.success(request, f"You are logged in as {username}")
                return redirect('tweet_list')
        else:
            messages.error(request, "invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'twitter/login.html', {'form': form})
    pass


def logout_request(request):
    logout(request)
    return redirect('tweet_list')

