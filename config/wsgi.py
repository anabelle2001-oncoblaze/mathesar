"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")


def strip_base_path(app, base_path):
    """
    Remove MATHESAR_BASE_PATH from the start of incoming request paths.

    Django only uses FORCE_SCRIPT_NAME when generating URLs, and expects the
    reverse proxy to have already removed the prefix from the request path.
    Stripping it here as well means Mathesar works behind reverse proxies that
    forward the full path, as well as those that remove the prefix.
    """
    def wrapped_app(environ, start_response):
        path_info = environ.get('PATH_INFO', '')
        if path_info == base_path or path_info.startswith(f'{base_path}/'):
            environ['PATH_INFO'] = path_info[len(base_path):] or '/'
        return app(environ, start_response)
    return wrapped_app


# Unlike get_wsgi_application(), django.setup() sets the URL script prefix from
# FORCE_SCRIPT_NAME. That way, URLs which are computed once when the
# application loads (such as the STATIC_URL used by WhiteNoise and the static
# files storage) include MATHESAR_BASE_PATH.
django.setup()
application = get_wsgi_application()

if settings.MATHESAR_BASE_PATH:
    application = strip_base_path(application, settings.MATHESAR_BASE_PATH)
