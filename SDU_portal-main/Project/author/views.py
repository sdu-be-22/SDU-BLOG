
from urllib import request
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
import os
from .forms import *
from .models import *
from .utils import *

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect('register')
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="registration/register.html", context={"register_form":form})

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

def profile(request, author_id):
    author = User.objects.get(username=author_id).pk
    dests = Blogs.objects.filter(author_id=author)
    adam = dests[0].author_id
    return render(request, 'author/profile.html', {'dests': dests,  'adam':adam})


def openBlog(request):
    print("here")
    return render(request, 'author/newBlog.html', {'form': BlogForm()})



class BlogView(FormView):
    template_name = '/author/newBlog.html'
    form_class = BlogForm
    success_url = '/'

    def form_valid(self, form):
        form.create_obj(self.request.user)
        return super().form_valid(form)


def deleteBlog(request,pk):
    form = Blogs.objects.get(id=pk)
    if len(form.img_url) > 0:
                os.remove(form.img_url.path)
    form.delete()
    return redirect('/')

def EditBlogView(request,pk):
    blog = Blogs.objects.get(id=pk)

    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(blog.img_url) > 0:
                os.remove(blog.img_url.path)
            blog.img_url = request.FILES['image']
        blog.title = request.POST.get('title')
        blog.description = request.POST.get('description')
        blog.save()
        messages.success(request, "Succ")   
        return redirect('profile', blog.author_id)

    context ={'blog':blog}
    return render(request,'author/editBLog.html',context)
   

def search(request):
        searched = request.GET.get('searched')
        
        if request.method == "POST":
            searched = request.POST['searched']
            blogs = Blogs.objects.filter(title__contains=searched)     
        
            return render(request,
                'author/search.html',
                {'searched':searched,
                  'blogs':blogs})
        elif request.method == "POST":
            searched = request.POST['searched']
            blogs = Blogs.objects.filter(title__contains!=searched)     
        
            return render(request,
            'author/search.html')
   
        

