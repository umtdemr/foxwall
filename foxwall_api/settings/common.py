from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


from .base import *  # noqa


try:
    from .prod import *  # noqa
except ImportError:
    from .dev import *  # noqa


# Other settings...

AUTH_USER_MODEL = "user.User"


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


REST_FRAMEWORK = {
    # OTHER SETTINGS
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'user.backends.JWTAuthentication',
    ),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Foxwall API',
    'DESCRIPTION': 'The Foxwall Social Network API',
    'VERSION': '1.0.0',
    "SERVE_INCLUDE_SCHEMA": False,
    "CONTACT": {
        "name": "Umit Demir",
        "email": "umitde296@gmail.com",
        "url": "https://umitde.com",
    },
    'COMPONENT_SPLIT_REQUEST': True
}


JWT_SECRET_KEY = ")N2gkxt^VVBkqkt96BzJkPLffQmA4P89GB7iR5s6oH(vwK$(%o"


MAX_USERNAME_LENGTH = 30
MAX_PASSWORD_LENGTH = 20
MIN_PASSWORD_LENGTH = 6
MAX_PROFILE_NAME_LENGTH = 25
MAX_PROFILE_AVATAR_SIZE = 10485760
MAX_PROFILE_COVER_SIZE = 10485760
PASSWORD_RESET_TIMEOUT_DAYS = 1


try:
    from .additional import *  # noqa
except Exception:
    pass
