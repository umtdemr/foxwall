from .common import BASE_DIR

SECRET_KEY = "django-insecure-bu+)thz_s+&mol(m!+bzex&nj3xpq52!4mm^=3f1zj76hf_=2v"

DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
