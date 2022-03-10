from fileinput import FileInput
from logging import PlaceHolder
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ImageField, ModelForm, TextInput, Textarea
from django.contrib.auth.models import User

# from Project import author
from .models import Blogs
from django.core.exceptions import ValidationError

from .models import *


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', 'placeHolder': 'Login'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeHolder': 'Password'}))


class BlogForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    img_url = forms.ImageField()

    def create_obj(self, something):
        title = self.cleaned_data['title']
        img_url = self.cleaned_data['img_url']
        description = self.cleaned_data['description']
        Blogs.objects.create(title=title, img_url=img_url, description=description, author_id=something)
        
        
        
class NewUserForm(UserCreationForm):
    email= forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username" , "email" , "password1" , "password2")
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
            return user

def __init__(self, *args, **kwargs):
    super(NewUserForm, self).__init__(*args, **kwargs)
    self.fields['username'].widget.attrs['class'] = 'form-control'
    self.fields['email'].widget.attrs['class'] = 'form-control'
    self.fields['password1'].widget.attrs['class'] = 'form-control'
    self.fields['password2'].widget.attrs['class'] = 'form-control'
