from django.urls import path
from .views import Login, Register, Logout, MyProfile

urlpatterns = [
  path('login/', Login.as_view(), name="login"),
  path('register/', Register.as_view(), name="register"),
  path('logout/', Logout.as_view(), name="logout"),
  path('my_profile/', MyProfile.as_view(), name="my_profile"),
]