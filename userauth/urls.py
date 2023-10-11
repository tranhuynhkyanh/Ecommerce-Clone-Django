from django.urls import path
from .views import register_view,login_view,logout_view,follow,profile_view,edit_profile,MessageView
from chat.views import index,chatPage
app_name = "userauth"
urlpatterns = [
    path("register/",register_view,name="register"),
    path("login/",login_view,name="login"),
    path("logout/",logout_view,name="logout"),
    path("follow/<vid>/",follow,name="follow"),
    path("",profile_view,name="profile"),
    path("update/",edit_profile,name="profile-update"),
    path("inbox/",index,name="chat"),
    path("chat-user/<uid>/",chatPage,name="chat-page"),

]
