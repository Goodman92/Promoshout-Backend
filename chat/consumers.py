from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from core.models import User
from .models import Channel
import json


class ConnectionsConsumer(WebsocketConsumer):
    def connect(self):
        # Is user author of this connection?
        connection_id = self._get_connection_id()

        # Get from request
        user = User.objects.get(id=connection_id)

        Channel.objects.retrieve_existing_channel_or_create(user, self.channel_name)
        self.accept()

    def disconnect(self, code):
        # User might have multiple channels, remove them all.
        Channel.objects.filter(name=self.channel_name).delete()

    def receive(self, text_data=None, bytes_data=None):
        print("ConnectionsConsumer.receive")
        print(self.channel_name)

        payload = json.loads(text_data)
        message = payload.get('message')

        connection_id = self._get_connection_id()
        # Get this information from the payload
        receiver = 1 if connection_id == "2" else 2
        channels = Channel.objects.filter(user__in=[receiver, connection_id])

        print(channels.values())
        for channel in channels:
            async_to_sync(self.channel_layer.send)(
                channel.name,
                {
                    "type": 'connection_message',
                    "message": message
                }
            )

    def connection_message(self, event):
        print("ConnectionsConsumer.connection_message")
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))

    def _get_connection_id(self):
        return self.scope.get('url_route', {}).get('kwargs', {}).get('id')


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Accept connection, is user connected with the another user?
        # Connection could happen based on receivers user id
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))
