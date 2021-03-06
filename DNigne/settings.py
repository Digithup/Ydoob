"""
Django settings for DNigne project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
from typing import List


from django.conf import settings
from django.contrib import messages

import notification.apps

STRIPE_API_KEY_PUBLISHABLE = "pk_test_51HIHiuKBJV2qfWbD2gQe6aqanfw6Eyul5P02KeOuSR1UMuaV4TxEtaQyzr9DbLITSZweL7XjK3p74swcGYrE2qEX00Hz7GmhMI"
STRIPE_API_KEY_HIDDEN = "sk_test_51HIHiuKBJV2qfWbD4I9pAODack7r7r9LJOY65zSFx7jUUwgy2nfKEgQGvorv1p2xP7tgMsJ5N9EW7K1lBdPnFnyK00kdrS27cj"

RAZORPAY_API_KEY_PUBLISHABLE = "rzp_test_Wj7ujrjP6ULkuq"
RAZORPAY_API_KEY_HIDDEN = "WT8djoNtYSAzA28BrhryFL0f"

PAYPAL_API_KEY_PUBLISHABLE = "Ab5gaq5YlFHQTAgbcIW79GV4wE7ObsefiPyNMNV87z1-2JzdNhHpOfGKIduOM1qItLgLI3eA2Z3PIHLw"
PAYPAL_API_KEY_HIDDEN = "aEKFH985N2oOIFWOeS7rdq2Nht6CdztTVDDjDuQCMIBKcAbjyL-Z3ZY9DeznZSaFbQTp1H4o7CrxgwjX4x"
import os
import tempfile
from pathlib import Path
import environ
import django_heroku

from django.contrib.messages import constants as message_constants
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for Productsion
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in Productsion secret!
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in Productsion!
DEBUG = env('DEBUG')

ALLOWED_HOSTS: List[str] = ['127.0.0.1', 'dnigne.herokuapp.com', '192.168.1.3','business.localhost']

ROOT_URLCONF = 'DNigne.urls'

AUTH_USER_MODEL = 'user.User'
# ALLOWED_HOSTS = [
#
# ]
# Application definition

INSTALLED_APPS = [

    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # eEXTERNAL  APPS

]

THIRD_PARTY_APPS = [
    'ckeditor',
    'ckeditor_uploader',
    'mptt',
    'rest_framework',
    'corsheaders',
    'crispy_forms',
    'rosetta',
    'parler',
    'currencies',
    'social_django',
    'whitenoise.runserver_nostatic',
    'formtools',
    'notification',
    'channels',
    "bootstrap4",
    "bootstrap_datepicker_plus",
    'import_export',



]
OWN_APPS = [
    ## internal apps
    'core.apps.CoreConfig',
    'catalog.apps.CatalogConfig',
    'coupons.apps.CouponsConfig',
    'invoice.apps.InvoiceConfig',
    'localization.apps.LocalizationConfig',
    'home.apps.HomeConfig',
    # 'media.apps.MediaConfig',
    'reports.apps.ReportsConfig',
    'sales.apps.SalesConfig',
    'vendors.apps.VendorsConfig',
    'user.apps.UserConfig',
    'billing',
    'DeliverySystem',
    'helper',

]

INSTALLED_APPS += THIRD_PARTY_APPS + OWN_APPS
CRISPY_TEMPLATE_PACK = 'bootstrap4'

DJANGO_NOTIFICATIONS_CONFIG = {'USE_JSONFIELD': True}

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',


    # 'whitenoise.middleware.WhiteNoiseMiddleware',

]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated usersaaa.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',

    ]
}
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
                'django.template.context_processors.i18n',
                'core.context_processors.core_processors',
                'core.context_processors.admin_summary',
                'core.context_processors.admin_chart',
                'home.context_processors.home_processors',
                'home.context_processors.user_processors',
                'home.context_processors.filter_processors',
                'home.context_processors.language_processors',
                'sales.context_processors.cart',
                'vendors.context_processors.vendor_processors',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'currencies.context_processors.currencies',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'notification.context_processors.notifications'

            ],
        },
    },
]
AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#                 'default': {
#
#                     'ENGINE': 'django.db.backends.mysql',
#                     'NAME': env('DB_NAME'),
#                     'USER': env('DB_USER'),
#                     'PASSWORD': env('DB_PASSWORD'),
#                     'HOST': env('DB_HOST'),
#                     'PORT': env('DB_PORT'),
#                 }
#             },

# if DEBUG:
DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# DATABASES = {
#         'default': {
#
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': env('server_DB_NAME'),
#             'USER': env('server_DB_USER'),
#             'PASSWORD': env('server_DB_PASSWORD'),
#             'HOST': env('server_DB_HOST'),
#             'PORT': env('server_DB_PORT'),
#         }
#     }
#


# if 'RDS_DB_NAME' in os.environ:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': os.environ['RDS_DB_NAME'],
#             'USER': os.environ['RDS_USERNAME'],
#             'PASSWORD': os.environ['RDS_PASSWORD'],
#             'HOST': os.environ['RDS_HOSTNAME'],
#             'PORT': os.environ['RDS_PORT'],
#         }
#     }
# else:
#     DATABASES = {
#         'default': {
#
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': env('DB_NAME'),
#             'USER': env('DB_USER'),
#             'PASSWORD': env('DB_PASSWORD'),
#             'HOST': env('DB_HOST'),
#             'PORT': env('DB_PORT'),
#         }
#     },
#

# python3 -c 'import psycopg2 as db; conn = db.connect("postgres://qjyolhgk:kHMr9gkyJ8gO-j2IBj7iZ2cFVql5nWpr@chunee.db.elephantsql.com/qjyolhgk"); print(conn.get_backend_pid()); conn.close()'


'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Egypt'
USE_I18N = True  # use internationalization
USE_L10N = True  # use localization
USE_TZ = True
gettext = lambda s: s
LANGUAGES = (
    ('en', _('English')),
    ('ar', _('Arabic')),

)
MODELTRANSLATION_LANGUAGES = ('en', 'ar')
LANGUAGE_COOKIE_NAME = 'django_language'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

DEFAULT_CURRENCY = 'USD'

# CUSTOM
FORCE_SESSION_TO_ONE = True  # Default is false

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
CSS_LOCATION = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/upload/'
MEDIA_ROOT = os.path.join(BASE_DIR, "upload")
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# enable/disable server cache
CACHES = {
    'default':
        {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'KEY_PREFIX': 'DNigne.Productsion',  # Change this
            'LOCATION': '127.0.0.1:11211',
            'TIMEOUT': 24 * 3600
        },
}

##  CKEDITOR CONFIGURATION ##
####################################

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"

###################################


CORS_ORIGIN_ALLOW_ALL = True
MESSAGE_LEVEL = message_constants.DEBUG
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
SITE_ID = 1

BASE_URL = "http://127.0.0.1:8000"

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
# SESSION_COOKIE_SECURE = True
LOGIN_URL = '/login'

LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/settings/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/settings/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

# Cart
CART_SESSION_ID = 'cart'
SESSION_COOKIE_AGE = 85555
SESSION_COOKIE_SECURE = False

WSGI_APPLICATION = 'DNigne.wsgi.application'
LOGOUT_REDIRECT_URL = '/'

# JET_INDEX_DASHBOARD = 'dashboard-bases.CustomIndexDashboard'

# email stuff
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'nigneegypt@gmail.com'
EMAIL_HOST_PASSWORD = 'Hitham5320826*'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_EMAIL_FROM = 'Multi Vendor Site <oreply@ydoob.com>'

SOCIAL_AUTH_FACEBOOK_KEY = '264061255547166'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'f472f0afb70fc84333e1d8e3bed58f84'  # App Secret

############Payment STRIPE########
STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = env('STRIPE_WEBHOOK_SECRET')

MyFatoorah_base_url = env('MyFatoorah_base_url')
MyFatoorah_api_key = env('MyFatoorah_api_key')
MyFatoorah_WEBHOOK_SECRET = env('MyFatoorah_WEBHOOK_SECRET')


FIREBASE_ADMIN_CREDENTIAL = os.path.join(BASE_DIR, "ydoob-ff08e-firebase-adminsdk-j7532-952cfe0721.json")
GOOGLE_MAP_API_KEY = "AIzaSyBxYTF5b1oobhbQo_dylaatAYm1BwARBb4"

PAYPAL_MODE = "sandbox"
PAYPAL_CLIENT_ID = "YOUR_PAYPAL_CLIENT_ID"
PAYPAL_CLIENT_SECRET = "YOUR_PAYPAL_CLIENT_SECRET"

NOTIFICATION_URL = "YOUR_HEROKU_URL"
ASGI_APPLICATION = "DNigne.asgi.application"
# Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": ['YOUR_HEROKU_REDIS_URL'],
        },
    },
}
