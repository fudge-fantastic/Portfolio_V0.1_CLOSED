"""
ASGI config for Portfolio project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Portfolio.settings")
application = get_asgi_application()