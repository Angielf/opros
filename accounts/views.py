from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .forms import UserRegistratrationForm
from django.contrib.auth.models import User


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect_url = request.GET.get('next', 'home')
            return redirect(redirect_url)
        else:
            messages.error(request, 'Неправильное имя или пароль')
    return render(request, 'accounts/login.html', {})


def logout_user(request):
    logout(request)
    return redirect('accounts:login')


def user_registration(request):
    if request.method == 'POST':
        form = UserRegistratrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username, email=email, password=password)
            messages.success(request, 'Вы зарегистрировались, {}'.format(user.username))
            return redirect('accounts:login')


    else:
        form = UserRegistratrationForm()
    return render(request, 'accounts/register.html', {'form': form})