from django.contrib.auth.models import User
from tabnanny import verbose
from django.db import models
from django.urls import reverse
from django.utils import timezone
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
       return self.name
    
    def get_absolute_url(self):
        return reverse('index') 

class Blogs(models.Model):
    title = models.CharField('Title name', max_length=255)
    description = models.TextField('Desc field')
    img_url = models.ImageField('Blog photo', upload_to='img/')
    author_id = models.ForeignKey(User, db_column="author_id", on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=255, default='none')
   
    def get_absolute_url(self):
        return reverse('index') 

    def __str__(self):
       return self.title

class Meta:
    verbose_name = "Blogs"
