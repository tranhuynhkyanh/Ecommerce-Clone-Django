from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.import datetime
from django.core.cache import cache
from django.conf import settings
import datetime

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
    def last_seen(self):
        return cache.get('seen_%s' % self.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                         seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False
        
class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")