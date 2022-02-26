import re
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *



class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))


def logout_user(request):
    print("there", request)
    logout(request)
    print("here",request)
    return redirect('/accounts/login')


def index(request):
    dests = Blogs.objects.all()
    return render(request, 'author/index.html', {'dests': dests})


def openBlog(request):
    print("here")
    return render(request, 'author/newBlog.html', {'form': BlogForm()})



class BlogView(FormView):
    template_name = 'author/newBlog.html'
    form_class = BlogForm

    def get(self, request):
        form = BlogForm()
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        
        form = BlogForm(request.POST,request.FILES)
        
        print(form.is_valid())
        if form.is_valid():
            blog = form.save(commit=True)
            print('something')
            dests = Blogs.objects.all()
            return render(request, 'author/index.html', {'dests': dests})

        args = {'form':form}
        return render(request, self.template_name, args)

   
        
