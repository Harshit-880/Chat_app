

# Set the default Django settings module for the 'asgi' application.


# Import and initialize Django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from myapp.routing import websocket_urlpatterns
from myapp.middleware import TokenAuthMiddleware






# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": URLRouter(
#         websocket_urlpatterns
#     ),
# })



application = ProtocolTypeRouter({

    "http": get_asgi_application(),
    "websocket":    
    # AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            
            TokenAuthMiddleware(
                URLRouter(
                    websocket_urlpatterns
                )
            )
        # )
        
    ),
})