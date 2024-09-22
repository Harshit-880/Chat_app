from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

@database_sync_to_async
def get_user(token_key):
    try:
        print("Retrieving user with token...")
        token = Token.objects.get(key=token_key)
        print(f"User found: {token.user.username}")
        return token.user
    except Token.DoesNotExist:
        print("Token does not exist, returning AnonymousUser.")
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    
    async def __call__(self, scope, receive, send):
        print(f"Middleware called with scope: {scope}")
        query_string = scope['query_string'].decode()
        print(f"Query string received: {query_string}")
        
        token_key = None
        for part in query_string.split('&'):
            if part.startswith('token='):
                token_key = part.split('=')[1]
                print(f"Token extracted: {token_key}")
                break
        
        scope['user'] = await get_user(token_key)
        print(f"User set in scope: {scope['user']}")
        
        return await super().__call__(scope, receive, send)
