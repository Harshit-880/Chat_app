# from channels.generic.websocket import WebsocketConsumer
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# import json
# from django.contrib.auth.models import User
# from .models import Contact, OnlineStatus
# from django.db.models import Q
# from django.utils import timezone


# class ChatConsumer(WebsocketConsumer):
 
#     def connect(self):
#         print("WebSocket connected!")
#         self.accept()
#     # def connect(self):
#     #     print("Attempting to connect...")
#     #     self.user = self.scope["user"]
#     #     if self.user.is_anonymous:
#     #         self.close()
#     #     else:
#     #         self.room_name = f"user_{self.user.username}"
#     #         self.room_group_name = f"chat_{self.room_name}"

#     #         async_to_sync(self.channel_layer.group_add)(
#     #             self.room_group_name,
#     #             self.channel_name
#     #         )

#     #         self.accept()
#     #         self.update_online_status(True)
#     #         print(f"{self.user.username} connected and added to {self.room_group_name}")

    
#     def online_status(self, event):
#         online_status = event['online_status']
#         self.send(text_data=json.dumps({
#             'type': 'online_status',
#             'online_status': online_status
#         }))

#     def update_online_status(self, is_online):
#         status, created = OnlineStatus.objects.get_or_create(user=self.user)
#         status.is_online = is_online
#         status.last_seen = timezone.now()
#         status.save()
#         self.broadcast_online_status()
    
#     def disconnect(self, close_code):
#         if hasattr(self, 'room_group_name'):
#             async_to_sync(self.channel_layer.group_discard)(
#                 self.room_group_name,
#                 self.channel_name
#             )

#         self.update_online_status(False)
#         print(f"{self.user.username} disconnected from {self.room_group_name}")

#     def update_online_status(self, is_online):
#         status, created = OnlineStatus.objects.get_or_create(user=self.user)
#         status.is_online = is_online
#         status.last_seen = timezone.now()
#         status.save()
#         self.broadcast_online_status()

#     def broadcast_online_status(self):
#         online_status = {
#             user.username: {
#                 'is_online': user.onlinestatus.is_online,
#                 'last_seen': user.onlinestatus.last_seen.isoformat()
#             }
#             for user in User.objects.all()
#         }
#         async_to_sync(self.channel_layer.group_send)(
#             "online_status_broadcast",
#             {
#                 'type': 'online_status',
#                 'online_status': online_status
#             }
#         )





from channels.consumer import  SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer

class MySyncConsumer(SyncConsumer):
    def websoket_connect(self,event):
        print('Websoket connect ............',event)
        self.send({
            'type':'websoket.accept',
        })

    def websoket_receive(self,event):
        print('Message received',event)
        print(event['text'])
        self.send({
            'type':'websoket.send',
            'text':'Message send to client'
        })

    def websoket_disconnect(self,event):
        print('Message disconnect...',event)
        raise StopConsumer( )