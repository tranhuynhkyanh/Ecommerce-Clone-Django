from django.db import models
from django.contrib.auth import get_user_model
from userauth.models import User
# Create your models here.

User = get_user_model()

class ChatModel(models.Model):
    sender = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="sender")
    receiver = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="receiver")
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.message