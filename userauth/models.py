from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.id,filename)
class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to=user_directory_path,null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self) :
        return self.email

class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")