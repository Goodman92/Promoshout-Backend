from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import chat.routing

# https are added by default
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlspatters))
})