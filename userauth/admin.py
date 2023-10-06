from django.contrib import admin
from .models import User,Follow
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email']
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower','following']
admin.site.register(User,UserAdmin)
admin.site.register(Follow,FollowAdmin)