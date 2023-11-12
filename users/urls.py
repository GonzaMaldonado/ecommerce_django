from django.urls import path
from .views import Login, register, Logout

urlpatterns = [
  path('login/', Login.as_view(), name="login"),
  path('register/', register, name="register"),
  path('logout/', Logout.as_view(), name="logout"),
]