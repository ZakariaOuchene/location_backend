# from channels.routing import ProtocolTypeRouter , URLRouter
# from channels.security.websocket   import AllowedHostsOriginValidator


# from django.urls import path

# from ecommerce_api.consumers import ChatConsumer



# application = ProtocolTypeRouter({
#     'websocket'   :AllowedHostsOriginValidator(
#         URLRouter({
#             path(''  , ChatConsumer)
#         })
#     )
# })




# chat/routing.py
from django.urls import re_path , path

from ecommerce_api.consumers import ChatConsumer, NotificationConsumer

# websocket_urlpatterns = [
#     re_path(r"ws/socket-server/", ChatConsumer.as_asgi()),
# ]

websocket_urlpatterns = [
    path("chats/<conversation_name>/", ChatConsumer.as_asgi()),
        path("notifications/", NotificationConsumer.as_asgi()),

]