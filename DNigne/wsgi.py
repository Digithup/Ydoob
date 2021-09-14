"""
WSGI config for DNigne project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DNigne.settings')

# application = ProtocolTypeRouter({
#     "https": get_asgi_application(),
#     # Just HTTP for now. (We can add other protocols later.)
# })

