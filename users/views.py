from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


class Login(View):

  def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'User authenticated') 
            return redirect('home')
        return render(request, 'users/login.html')
  
  def post(self, request):
     username = request.POST.get('username')
     password = request.POST.get('password')
     user = authenticate(username=username, password=password)

     if user:
        login(request, user)
        messages.success(request, f'Welcome back {username}!')
        return redirect('home')
     messages.success(request, 'Username or password does not match!')
     return render(request, 'users/login.html')


def register(request):
  pass
  #return render(request, 'users/register.html')


class Logout(View):

  def get(self, request, *args, **kwargs):
    logout(request)
    messages.success(request, 'See you later!')
    return redirect('login')