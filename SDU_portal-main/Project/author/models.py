from django.contrib.auth.models import User
from tabnanny import verbose
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
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
    likes = models.ManyToManyField(User, related_name='blogpost_like')
    blog_views = models.IntegerField(default=0, null=True)
    
    def number_of_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('index') 

    def __str__(self):
       return self.title

class Comment(models.Model):
    post = models.ForeignKey(Blogs, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '%s - %s' % (self.post, self.body)

class ProfileInfo(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=55, blank=True, null=True)
    last_name = models.CharField(max_length=55, blank=True, null=True)
    img_pro = models.ImageField(upload_to='img/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    phone_num = models.CharField(max_length=55, blank=True, null=True)
    city = models.CharField(max_length=55, blank=True, null=True)
    address = models.CharField(max_length=55, blank=True, null=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):
        return '%s : %s' % (self.user, self.first_name)

class Meta:
    verbose_name = "Blogs"
