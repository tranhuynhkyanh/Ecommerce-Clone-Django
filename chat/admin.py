from django.contrib import admin
from chat.models import ChatModel
# Register your models here.
class ChatModelAdmin(admin.ModelAdmin):
    list_display = ['sender','receiver','message','timestamp']
admin.site.register(ChatModel)