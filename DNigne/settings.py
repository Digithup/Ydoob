"""
Django settings for DNigne project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

STRIPE_API_KEY_PUBLISHABLE = "pk_test_51HIHiuKBJV2qfWbD2gQe6aqanfw6Eyul5P02KeOuSR1UMuaV4TxEtaQyzr9DbLITSZweL7XjK3p74swcGYrE2qEX00Hz7GmhMI"
STRIPE_API_KEY_HIDDEN = "sk_test_51HIHiuKBJV2qfWbD4I9pAODack7r7r9LJOY65zSFx7jUUwgy2nfKEgQGvorv1p2xP7tgMsJ5N9EW7K1lBdPnFnyK00kdrS27cj"

RAZORPAY_API_KEY_PUBLISHABLE = "rzp_test_Wj7ujrjP6ULkuq"
RAZORPAY_API_KEY_HIDDEN = "WT8djoNtYSAzA28BrhryFL0f"

PAYPAL_API_KEY_PUBLISHABLE = "Ab5gaq5YlFHQTAgbcIW79GV4wE7ObsefiPyNMNV87z1-2JzdNhHpOfGKIduOM1qItLgLI3eA2Z3PIHLw"
PAYPAL_API_KEY_HIDDEN = "aEKFH985N2oOIFWOeS7rdq2Nht6CdztTVDDjDuQCMIBKcAbjyL-Z3ZY9DeznZSaFbQTp1H4o7CrxgwjX4x"
import os
import tempfile
from pathlib import Path

from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jwv-s5yx#u7bhnxh6zjt3ds=!jnvqv(qv5zu!2$g)t)n*d8zf+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home.apps.HomeConfig',

    # Admin APPS
    'catalog.apps.CatalogConfig',
    'coupons.apps.CouponsConfig',
    'invoice.apps.InvoiceConfig',
    'localization',
    'media.apps.MediaConfig',
    'reports.apps.ReportsConfig',
    'sales.apps.SalesConfig',
    'vendors.apps.VendorsConfig',
    # internal apps
    'accounts',
    'core',
    'billing',

    # internal apps
    'widget_tweaks',
    'ckeditor',
    'ckeditor_uploader',
    "bootstrap4",
    'jet.dashboard',
    'jet',
    'easy_thumbnails',
    'filer',
    'mptt',
    'whoosh',
    'haystack',
    'rest_framework',
    'corsheaders',
    'crispy_forms',
    'easy_select2',
    'multiselectfield',
    'imagefit',
    'imagekit',
    'modeltranslation',
    'jquery',
    'djangoformsetjs',

]
CRISPY_TEMPLATE_PACK = 'bootstrap4'
AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',

]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated usersaaa.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',

    ]
}

WHOOSH_INDEX = os.path.join(BASE_DIR, 'whoosh/')

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

ROOT_URLCONF = 'DNigne.urls'
# JET_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR / 'templates')]

        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'core.context_processors.site_profile',
                'sales.context_processors.cart',
                # 'vendors.context_processors.user_profile',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'DNigne.wsgi.application'
LOGOUT_REDIRECT_URL = '/admin'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DNigne',
        'USER':'root',
        'PASSWORD':'',
        'Host':'localhost',
        'PORT':'3306',
    }
}
'''

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/



# dynamic data translate
_ = lambda s: s
LANGUAGES = (
    ('en', _('English')),
    ('ar', _('Arabic')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
# MODELTRANSLATION_LANGUAGES = ('en', 'de', 'tr')
LANGUAGE_COOKIE_NAME=''

DEFAULT_CURRENCY = 'USD'
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_I18N = True  # use internationalization
USE_L10N = True  # use localization
USE_TZ = True

# CUSTOM
FORCE_SESSION_TO_ONE = True  # Default is false

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
IMAGEFIT_ROOT = "upload"
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),

]

MEDIA_URL = '/upload/'
MEDIA_ROOT = os.path.join(BASE_DIR, "upload")

# enable/disable server cache

IMAGEFIT_CACHE_ENABLED = True
# set the cache name specific to imagefit with the cache dict
IMAGEFIT_CACHE_BACKEND_NAME = 'imagefit'
CACHES = {

    'default':

        {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'KEY_PREFIX': 'DNigne.production',  # Change this
            'LOCATION': '127.0.0.1:11211',
            'TIMEOUT': 24 * 3600

        },
    'imagefit': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(tempfile.gettempdir(), 'django_imagefit')
    },
}

IMAGEFIT_PRESETS = {
    'thumbnail': {'width': 64, 'height': 64, 'crop': True},
    'my_preset1': {'width': 300, 'height': 220},
    'my_preset2': {'width': 100},
}
# ...
SITE_ID = 1

####################################
##  CKEDITOR CONFIGURATION ##
####################################

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"

###################################


CORS_ORIGIN_ALLOW_ALL = True

# email stuff
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Cart
CART_SESSION_ID = 'cart'
SESSION_COOKIE_AGE = 86400
