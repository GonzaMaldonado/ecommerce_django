from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect

from .forms import RegisterForm

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


class Register(View):

  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
       return redirect('home')
    return render(request, 'users/register.html', {'form': RegisterForm})
     
  def post(self, request):
     form = RegisterForm(request.POST)

     if form.is_valid():
        user = form.save(commit=False)
        user.email = user.email.lower()
        user.save()
        login(request, user)
        messages.success(request, f'Welcome {user.username}!')
        return redirect('home')
     
     error_text = form.errors.as_text()
     error = error_text.split('*')
     messages.success(request, f'{error[2]}')
     return HttpResponseRedirect((request.META.get('HTTP_REFERER')))



class Logout(View):

  def get(self, request, *args, **kwargs):
    logout(request)
    messages.success(request, 'See you later!')
    return redirect('login')


class MyProfile(View):
   def get(self, request, *args, **kwargs):
      return render(request, 'users/profile.html')