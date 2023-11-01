from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import ChatModel
from userauth.models import User
# Create your views here.


def index(request):
   # users = User.objects.exclude(id=request.user.id)
    #users = User.objects.exclude(username=request.user.username)
    print(ChatModel.objects.filter(sender=request.user).all().values_list("receiver_id",flat=True))
    users = User.objects.filter(id__in=ChatModel.objects.filter(sender=request.user).all().values_list("receiver_id",flat=True))
    user_obj = User.objects.get(id=ChatModel.objects.filter(sender=request.user).all().values_list("receiver_id",flat=True).order_by("timestamp").first())
    print(user_obj)
    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name = f'chat_{user_obj.id}-{request.user}'
    message_objs = ChatModel.objects.filter(sender__in=[request.user,user_obj],receiver__in=[request.user,user_obj])
    print(message_objs)
    return render(request, 'chat/base.html', context={'first_user': user_obj,'users': users, 'messages': message_objs})


def chatPage(request, uid):
    user_obj = User.objects.get(id=uid)
    users = User.objects.filter(id__in=ChatModel.objects.filter(sender=request.user).all().values_list("receiver_id",flat=True))
    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'
    message_objs = ChatModel.objects.filter(thread_name=thread_name)
    return render(request, 'chat/chat.html', context={'user': user_obj, 'users': users, 'messages': message_objs})