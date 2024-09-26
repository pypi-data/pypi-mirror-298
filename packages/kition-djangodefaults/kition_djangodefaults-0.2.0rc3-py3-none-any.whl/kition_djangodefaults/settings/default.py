import os

from django.core.management.utils import get_random_secret_key

from .default_basedir import BASE_DIR

DEBUG = os.getenv("DEBUG", "false").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())

ALLOWED_HOSTS = [
    os.getenv("ALLOWED_HOSTS", "localhost"),
]

if os.getenv("CSRF_TRUSTED_ORIGIN"):
    CSRF_TRUSTED_ORIGINS = [os.getenv("CSRF_TRUSTED_ORIGIN")]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
TLS_ENABLED = os.getenv("TLS_ENABLED", "false").lower() == "true"
if TLS_ENABLED:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "3600"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = (
        os.getenv("SECURE_HSTS_INCLUDE_SUBDOMAINS", "false").lower() == "true"
    )
    SECURE_HSTS_PRELOAD = os.getenv("SECURE_HSTS_PRELOAD", "false").lower() == "true"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DATABASE_NAME", "app"),
        "USER": os.getenv("DATABASE_USER", "postgres"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", "app"),
        "HOST": os.getenv("DATABASE_HOST", "localhost"),
        "PORT": os.getenv("DATABASE_PORT", 5432),
        "CONN_MAX_AGE": 0,
    }
}

# E-Mail / SMTP
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@example.com")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 1025))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "false").lower() == "true"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Storage
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
    "default": {},
}

OBJECT_STORAGE_ENABLED = os.getenv("OBJECT_STORAGE_ENABLED", "false").lower() == "true"
if OBJECT_STORAGE_ENABLED:
    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": os.getenv("STORAGE_BUCKET_NAME", "app"),
            "endpoint_url": os.getenv("STORAGE_ENDPOINT", "http://localhost:9000"),
            "region_name": os.getenv("STORAGE_REGION", "eu-central-1"),
        },
    }
else:
    STORAGES["default"] = {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    }
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    MEDIA_URL = "/media/"
