"""
ASGI config for Ecommerce project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os,django
from Ecommerce.wsgi import *
from django.urls import path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.consumers import *
from channels.auth import AuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Ecommerce.settings")
django.setup()


application = ProtocolTypeRouter({
    "https": get_asgi_application(), 
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('chat/<int:id>/', PersonalChatConsumer.as_asgi()),
        ])
    )
})       