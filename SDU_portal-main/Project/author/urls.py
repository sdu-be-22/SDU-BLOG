
from django.conf import settings
from multiprocessing.dummy import Namespace
from xml.etree.ElementInclude import include
from django.urls import path
from . views import *
from django.contrib.auth import views as auth_views

from .  import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('/<str:pk>', views.index, name='index'),
    path('profile/<str:author_id>', views.profile, name='profile'),
    path('', LoginUser.as_view(), name='login'),
    path('logou1t/', views.logout_user, name='logou1t'),
    path('openBlog/', views.openBlog, name='goNewBlog'),
    path('/', BlogView.as_view(), name='addBlog'),
    path('openBlog/edit/<str:pk>', views.EditBlogView, name = 'editBlogs'),
    path('deleteBlog/<str:pk>', views.deleteBlog, name = 'deleteBlog'),
    path('register', views.register_request, name='register'),
    path('search', views.search, name='searching'),
    path('save-comment', views.save_comment, name='save-comment'),
    path('profile_info/', views.ProfileView.as_view(), name='profile-info'),
    path('password', views.change_password, name='change_password'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uib64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('like/<str:id>/', views.liked_blog, name='like-blog'),
    path('dislike/<str:id>/', views.dislike_blog, name='dislike-blog'),
] 
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

