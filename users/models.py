import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class User(AbstractUser, PermissionsMixin):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  username = models.CharField(max_length=50, unique=True)
  email = models.EmailField(max_length=75)
  photo = models.ImageField(default="user.png", upload_to='users/', null=True, blank=True)
  date_joined = models.DateTimeField(auto_now_add=True)

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email']

  class Meta:
    ordering = ['-date_joined']

  def __str__(self) -> str:
    return self.username