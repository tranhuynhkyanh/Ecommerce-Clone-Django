from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import ChatModel
from userauth.models import User
# Create your views here.




def index(request):
   # users = User.objects.exclude(id=request.user.id)
    
    users = User.objects.exclude(username=request.user.username)
    return render(request, 'chat/base.html', context={'users': users})


def chatPage(request, uid):
    user_obj = User.objects.get(id=uid)
    users = User.objects.exclude(username=request.user.username)
    
    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'
    message_objs = ChatModel.objects.filter(thread_name=thread_name)
    return render(request, 'chat/chat.html', context={'user': user_obj, 'users': users, 'messages': message_objs})