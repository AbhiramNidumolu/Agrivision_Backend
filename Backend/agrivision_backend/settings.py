import os
from pathlib import Path

# -----------------------
# BASE CONFIGURATION
# -----------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-test-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]  # For development; restrict later for production

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",

    # Local apps
    "users",
    "images.apps.ImagesConfig",  # ✅ Use the AppConfig
]

# -----------------------
# MIDDLEWARE
# -----------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # Must come before CommonMiddleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "agrivision_backend.urls"

# -----------------------
# TEMPLATES
# -----------------------
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

WSGI_APPLICATION = "agrivision_backend.wsgi.application"

# -----------------------
# DATABASE (PostgreSQL)
# -----------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "agrivision_db",
        "USER": "postgres",
        "PASSWORD": "2005",  # Change to your DB password
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# -----------------------
# PASSWORD VALIDATION
# -----------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------
# INTERNATIONALIZATION
# -----------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"  # local timezone
USE_I18N = True
USE_TZ = True

# -----------------------
# STATIC FILES
# -----------------------
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------
# AUTH & DRF CONFIG
# -----------------------
AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# -----------------------
# CORS (for React Frontend)
# -----------------------
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-csrftoken",
    "x-requested-with",
]

# -----------------------
# EMAIL BACKEND (for OTPs)
# -----------------------
# Option 1: For Local Testing (prints OTP in console)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Option 2: For Real Emails via Gmail (Uncomment when ready)
"""
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "20abhiram05@gmail.com"
EMAIL_HOST_PASSWORD = "pqhb mqev wahq tavf"
"""

DEFAULT_FROM_EMAIL = "AgriVision <noreply@agrivision.com>"
