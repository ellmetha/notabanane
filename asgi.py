"""
    ASGI application used by the notabanane project
    ===============================================

    This module contains the ASGI application used by Django's development server and any production
    ASGI deployments. It should expose a module-level variable named ``application``.

"""

from django.core.asgi import get_asgi_application


application = get_asgi_application()
