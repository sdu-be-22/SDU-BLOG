from tabnanny import verbose
from django.db import models
from django.urls import reverse

# Create your models here.
class Blogs(models.Model):
    title = models.CharField('Title name', max_length=255)
    description = models.TextField('Desc field')
    img_url = models.ImageField('Blog photo', upload_to='img/')
    date = models.DateTimeField(auto_now_add=True)

def __str__(self):
       return self.title

class Meta:
    verbose_name = "Blogs"