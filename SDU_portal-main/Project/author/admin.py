from django.contrib import admin
from .models import Blogs, Category,Comment, ProfileInfo

# Register your models here.
admin.site.register(Blogs)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(ProfileInfo)