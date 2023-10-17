from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.import datetime
from django.core.cache import cache
import datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Ecommerce.settings")

def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.id,filename)
class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to=user_directory_path,null=True,default="none.jpg")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self) :
        return self.email

class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")