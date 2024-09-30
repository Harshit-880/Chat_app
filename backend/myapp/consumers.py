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





# from channels.consumer import  SyncConsumer
# from channels.exceptions import StopConsumer


# class MySyncConsumer(SyncConsumer):
#     def websocket_connect(self, event):
#         print('WebSocket connected:', event)
#         self.send({
#             'type': 'websocket.accept',
#         })

#     def websocket_receive(self, event):
#         print('Message received:', event)
#         print('Received text:', event['text'])
#         self.send({
#             'type': 'websocket.send',
#             'text': 'Message sent to client'
#         })


#     def websocket_disconnect(self, event):
#         print('WebSocket disconnected:', event)
#         raise StopConsumer()


# from channels.generic.websocket import WebsocketConsumer

# class MySyncConsumer(WebsocketConsumer):
#     def connect(self):
#         # Accept the WebSocket connection
#         self.accept()
#         print("WebSocket connected ............ new")

#     def disconnect(self, close_code):
#         # Handle WebSocket disconnection
#         print("WebSocket disconnected ............... new")

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from .models import Contact, OnlineStatus
import json
from django.utils import timezone

class ChatConsumer(WebsocketConsumer):
    # def connect(self):
    #     # Retrieve the user from the scope, which is set by the middleware
    #     user = self.scope.get('user', None)

    #     # Check if the user is authenticated and not anonymous
    #     if user and not user.is_anonymous:
    #         self.accept()  # Accept the WebSocket connection
    #         print(f"WebSocket connected: User - {user.username}")
    #     else:
    #         # Reject the connection if no authenticated user is found
    #         print("WebSocket connection rejected: User is anonymous or not found.")
    #         self.close()  # Close the WebSocket connection
    def connect(self):
        self.user = self.scope["user"]
        print(f"User found: {self.user}")

        if self.user.is_anonymous:
            print("Anonymous user detected, closing connection.")
            self.close()
        else:
            self.room_name = f"user_{self.user.username}"
            self.room_group_name = f"chat_{self.room_name}"
            print(f"Room name: {self.room_group_name}")

            # Adding the user to the room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            print(f"User {self.user.username} added to {self.room_group_name}")

            # Updating online status
            try:
                self.update_online_status(True)
                print(f"Updated online status for {self.user.username}")
            except Exception as e:
                print(f"Error updating online status: {e}")

            self.accept()
            print(f"{self.user.username} connected and added to room {self.room_group_name}")


    def disconnect(self, close_code):
        # Handle disconnection
        print(f"WebSocket disconnected for user {self.user.username if self.user else 'unknown'}")
        if hasattr(self, 'room_group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )
        self.update_online_status(False)
        print(f"User {self.user.username} removed from {self.room_group_name} and status updated to offline.")

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        contact_username = data.get('contact')

        if message and contact_username:
            try:
                contact_user = User.objects.get(username=contact_username)
                if Contact.objects.filter(user=self.user, contact=contact_user, accepted=True).exists() or Contact.objects.filter(user=contact_user, contact=self.user, accepted=True).exists():
                    sender_room_group_name = f"chat_user_{self.user.username}"
                    recipient_room_group_name = f"chat_user_{contact_username}"

                    async_to_sync(self.channel_layer.group_send)(
                        recipient_room_group_name,
                        {
                            'type': 'chat_message',
                            'message': message,
                            'sender': self.user.username,
                        }
                    )

                    print(f"Message routed to {recipient_room_group_name}")
            except User.DoesNotExist:
                self.send(text_data=json.dumps({'error': 'Contact user does not exist.'}))
                print(f"Failed to find user {contact_username}")


    def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'type': 'chat_message'
        }))

    def update_online_status(self, is_online):
        print(f"Updating online status for {self.user.username}: {is_online}")
        # Check if OnlineStatus object exists, create if not
        status, created = OnlineStatus.objects.get_or_create(user=self.user)
        print(f"OnlineStatus object {'created' if created else 'found'} for user {self.user.username}")

        status.is_online = is_online
        status.last_seen = timezone.now()
        status.save()
        print(f"Online status saved for {self.user.username}: is_online={status.is_online}, last_seen={status.last_seen}")
        self.broadcast_online_status()


    def broadcast_online_status(self):
        print("Broadcasting online status...")
        try:
            # Collect online statuses of all users safely
            online_status = {}
            for user in User.objects.all():
                try:
                    # Try to access the onlinestatus object of the user
                    status = user.onlinestatus
                    online_status[user.username] = {
                        'is_online': status.is_online,
                        'last_seen': status.last_seen.isoformat()
                    }
                    print(f"Status found for user {user.username}: {online_status[user.username]}")
                except OnlineStatus.DoesNotExist:
                    # Handle the case where onlinestatus does not exist for the user
                    print(f"No OnlineStatus found for user {user.username}. Skipping.")

            # If there is any status to broadcast
            if online_status:
                async_to_sync(self.channel_layer.group_send)(
                    "online_status_broadcast",
                    {
                        'type': 'online_status',
                        'online_status': online_status
                    }
                )
                print("Online status broadcast sent successfully.")
            else:
                print("No online statuses available to broadcast.")

        except Exception as e:
            print(f"Error during broadcasting online status: {e}")



    def online_status(self, event):
        online_status = event['online_status']
        print(f"Received online status event: {online_status}")
        self.send(text_data=json.dumps({
            'type': 'online_status',
            'online_status': online_status
        }))
        print("Online status sent to WebSocket client.")



class OnlineStatusConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            self.close()
        else:
            self.room_group_name = "online_status_broadcast"
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()
            self.broadcast_online_status()
            print(f"{self.user.username} connected and added to {self.room_group_name}")
    
    def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )
        self.broadcast_online_status()

    def receive(self, text_data):
        pass

    def broadcast_online_status(self):
        print("Broadcasting online status...")
        try:
            # Collect online statuses of all users safely
            online_status = {}
            for user in User.objects.all():
                try:
                    # Try to access the onlinestatus object of the user
                    status = user.onlinestatus
                    online_status[user.username] = {
                        'is_online': status.is_online,
                        'last_seen': status.last_seen.isoformat()
                    }
                    print(f"Status found for user {user.username}: {online_status[user.username]}")
                except OnlineStatus.DoesNotExist:
                    # Handle the case where onlinestatus does not exist for the user
                    print(f"No OnlineStatus found for user {user.username}. Skipping.")

            # If there is any status to broadcast
            if online_status:
                async_to_sync(self.channel_layer.group_send)(
                    "online_status_broadcast",
                    {
                        'type': 'online_status',
                        'online_status': online_status
                    }
                )
                print("Online status broadcast sent successfully.")
            else:
                print("No online statuses available to broadcast.")

        except Exception as e:
            print(f"Error during broadcasting online status: {e}")
            #  that code not work because of i have a root user that do not exist in online status 

    def online_status(self, event):
        online_status = event['online_status']
        self.send(text_data=json.dumps({
            'type': 'online_status',
            'online_status': online_status
        }))