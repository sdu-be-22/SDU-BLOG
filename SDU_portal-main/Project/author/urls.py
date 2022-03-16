
from multiprocessing.dummy import Namespace
from xml.etree.ElementInclude import include
from django.urls import path
from . views import *
from .  import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('/<int:pk>', views.index, name='index'),
    path('profile/<str:author_id>', views.profile, name='profile'),
    path('', LoginUser.as_view(), name='login'),
    path('logou1t/', views.logout_user, name='logou1t'),
    path('openBlog/', views.openBlog, name='goNewBlog'),
    path('/', BlogView.as_view(), name='addBlog'),
    path('openBlog/edit/<str:pk>', views.EditBlogView, name = 'editBlogs'),
    path('deleteBlog/<str:pk>', views.deleteBlog, name = 'deleteBlog'),
    path('register', views.register_request, name='register'),
    path('search', views.search, name='searching'),
] 
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

