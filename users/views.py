from django.shortcuts import render

# Create your views here.
def login(request):
  return render(request, 'users/login.html')

def register(request):
  pass
  #return render(request, 'users/register.html')

def logout(request):
  pass