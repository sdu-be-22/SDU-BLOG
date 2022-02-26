from fileinput import FileInput
from logging import PlaceHolder
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ImageField, ModelForm, TextInput, Textarea
from django.contrib.auth.models import User
from .models import Blogs
from django.core.exceptions import ValidationError

from .models import *


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', 'placeHolder': 'Login'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeHolder': 'Password'}))


class BlogForm(forms.ModelForm):
     class Meta:
         model = Blogs
         fields = ('title', 'description','img_url',)
         widgets = {
            'title': TextInput(attrs={'class': 'form-input', 'placeHolder': 'Title'}),
            'description': Textarea(attrs={'cols': 30, 'rows': 10, 'placeholder': 'Description'}),
            # 'img_url': ImageField(name='imageFile')
        }