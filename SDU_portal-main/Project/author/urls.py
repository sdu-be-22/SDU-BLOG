
from multiprocessing.dummy import Namespace
from xml.etree.ElementInclude import include
from django.urls import path
from . views import *
from .  import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('', LoginUser.as_view(), name='login'),
    path('logou1t/', views.logout_user, name='logou1t'),
    path('openBlog/', views.openBlog, name='goNewBlog'),
    path('/', BlogView.as_view(), name='addBlog'),
] 
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)