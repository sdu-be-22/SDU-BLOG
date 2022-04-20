
import os
from urllib import request

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.paginator import Paginator
from django.http import (Http404, HttpResponse, HttpResponseNotFound,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)

import author

from .forms import *
from .forms import NewUserForm
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


class ContactListView(ListView):
    paginate_by = 2
    model = Blogs

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
    category_id = request.GET.get('category')
    if(category_id):
       dests = Blogs.objects.filter(category = category_id)
    else:
       dests = Blogs.objects.all()
    paginator = Paginator(dests, 2) # Show 25 contacts per page.
    # stuff = get_object_or_404(Blogs,id=self.kwargs['pk'])
    # total_likes = stuff.total_likes()
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    category = Category.objects.all()
    context = {'page_obj': page_obj, "category":category}
    return render(request, 'author/index.html', context)


def BlogPostLike(request, pk):
    post = get_object_or_404(Blogs, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('blogpost_like', args=[str(pk)]))

class BlogPostDetailView(DetailView):
    model = Blogs
         
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(BlogPost, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return data   

def profile(request, author_id):
    author = User.objects.get(username=author_id).pk
    dests = Blogs.objects.filter(author_id=author)
    try:
        adam = author
        context = {'dests': dests, 'adam': adam}
    except IndexError:
        context ={'dests': dests, 'adam': author}
    return render(request, 'author/profile.html', context)


def openBlog(request):
    print("here")
    return render(request, 'author/newBlog.html', {'form': BlogForm()})



class BlogView(FormView):
    template_name = 'author/newBlog.html'
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
        
            return render(request,'author/search.html')

def save_comment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        postid = request.POST['postid']
        blog = Blogs.objects.get(pk=postid)
        user = request.user

        Comment.objects.create(
            user = user,
            post = blog,
            body = comment
        )
    
    return JsonResponse({'bool':True})


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfileView(View):
    profile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = ProfileInfo.objects.get_or_create(user=request.user)
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'profile': self.profile, 'segment': 'profile'}
        return render(request, 'author/profile_info.html', context)

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=self.profile)
        profile = ProfileInfo(user=request.user)
        if form.is_valid():
            form.first_name = request.POST.get('first_name')
            form.last_name = request.POST.get('last_name')
            form.bio = request.POST.get('bio')

            form.img_pro = request.POST.get('img_pro')
            form.birthday = request.POST.get('birthday')
            form.phone_num  = request.POST.get('phone_num')
            form.city = request.POST.get('city')
            form.address = request.POST.get('address')
           
            profile = form.save()
            profile.user.save()

            messages.success(request, 'Profile saved successfully')
        else:
            messages.error(request, form_validation_error(form))
        return redirect('profile-info')



@login_required
def change_password(request):
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'author/password_change.html', {
        'form': form
    })

@login_required
def favorite_list(request):
    new = Blogs.objects.filter(favorites = request.user)
    print(new)
    return render(request, 'author/favorites.html', {'dests': new})



@login_required
def favorite_add(request, id):
    blog = get_object_or_404(Blogs, id=id)
    # print(blog)
    if blog.favorites.filter(id = request.user.id).exists():
        blog.favorites.remove(request.user)
    else:
        blog.favorites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

