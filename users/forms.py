from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ImageField, FileInput

from .models import User

class RegisterForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']

  def __init__(self, *args, **kwargs):
    super(RegisterForm, self).__init__(*args, **kwargs)
    self.fields['username'].widget.attrs['class'] = 'form-control text-dark small rounded-4 w-100'
    self.fields['email'].widget.attrs['class'] = 'form-control text-dark small rounded-4 w-100'
    self.fields['password1'].widget.attrs['class'] = 'form-control text-dark small rounded-4 w-100'
    self.fields['password2'].widget.attrs['class'] = 'form-control text-dark small rounded-4 w-100'
    self.fields['username'].widget.attrs['placeholder'] = 'Username'
    self.fields['email'].widget.attrs['placeholder'] = 'Email'
    self.fields['password1'].widget.attrs['placeholder'] = 'Password'
    self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'


class UpdateUserForm(ModelForm):
  photo = ImageField(widget=FileInput)
  class Meta:
    model = User
    fields = ['username', 'email', 'photo']

  def __init__(self, *args, **kwargs):
    super(UpdateUserForm, self).__init__(*args, **kwargs)
    self.fields['username'].widget.attrs['class'] = 'form-control text-dark text-sm rounded-2 d-block w-50 mx-auto'
    self.fields['email'].widget.attrs['class'] = 'form-control text-dark text-sm rounded-2 d-block w-50 mx-auto bg-body-secondary'
    self.fields['photo'].widget.attrs['class'] = 'form-control text-dark text-sm rounded-2 d-block w-50 mx-auto'
    
    self.fields['username'].widget.attrs['placeholder'] = 'Username'
    self.fields['email'].widget.attrs['placeholder'] = 'Email'
