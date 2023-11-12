from django.urls import path
from .views import Login, register, logout

urlpatterns = [
  path('login/', Login.as_view(), name="login"),
  path('register/', register, name="register"),
  path('logout/', logout, name="logout"),
]