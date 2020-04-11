from django.urls import path
from websocketapp.websocket import WbConsumer

websocket_urlpatterns = [
    path('ws/<int:e_id>', WbConsumer)
]