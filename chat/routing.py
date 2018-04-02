from django.conf.urls import url
from . import consumers

websocket_urlspatters = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer)
]