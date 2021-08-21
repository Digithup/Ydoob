"""
Django settings for DNigne project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import django_heroku
from django.conf import settings
from django.contrib import messages

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

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()
from django.contrib.messages import constants as message_constants
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for Productsion
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in Productsion secret!
SECRET_KEY ='jwv-s5yx#u7bhnxh6zjt3ds=!jnvqv(qv5zu!2$g)t)n*d8zf+'

# SECURITY WARNING: don't run with debug turned on in Productsion!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = [
    '127.0.0.1',
    'nigne.herokuapp.com'
]

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Admin APPS
    # 'debug_toolbar',
    'catalog.apps.CatalogConfig',
    'coupons.apps.CouponsConfig',
    'invoice.apps.InvoiceConfig',
    'localization.apps.LocalizationConfig',
    'home.apps.HomeConfig',
    'media.apps.MediaConfig',
    'reports.apps.ReportsConfig',
    'sales.apps.SalesConfig',
    'vendors.apps.VendorsConfig',
    'user.apps.UserConfig',
    'core.apps.CoreConfig',
    # internal apps

    'billing',
    # internal apps
    'widget_tweaks',
    'ckeditor',
    'ckeditor_uploader',
    "bootstrap4",
    # 'jet.dashboard-bases',
    # 'jet',
    'easy_thumbnails',
    'filer',
    'mptt',
    # 'whoosh',
    # 'haystack',
    'rest_framework',
    'corsheaders',
    'crispy_forms',
    'easy_select2',
    'multiselectfield',
    'imagefit',
    'imagekit',
    # 'modeltranslation',
    'rosetta',
    'translations',
    'parler',
    # 'django_database_translation',
    # 'jquery',
    # 'djangoformsetjs',
    'django_countries',
    'django_select2',
    'currencies',

]
CRISPY_TEMPLATE_PACK = 'bootstrap4'

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
                'home.context_processors.home_processors',
                'home.context_processors.user_processors',
                'home.context_processors.filter_processors',

                'sales.context_processors.cart',
                'vendors.context_processors.vendor_processors',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'currencies.context_processors.currencies',

            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dnigne',
        'USER': 'root',
        'PASSWORD': 'Hitham5320826*',
        'PORT': '3306',
        'HOST': '127.0.0.100'
    }
}

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
HAYSTACK_DOCUMENT_FIELD = 'text'
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
WHOOSH_INDEX = os.path.join(BASE_DIR, 'whoosh/')
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

# dynamic data translate
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
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
IMAGEFIT_ROOT = "public"
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),

]

MEDIA_URL = '/upload/'
MEDIA_ROOT = os.path.join(BASE_DIR, "upload")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# enable/disable server cache

IMAGEFIT_CACHE_ENABLED = True
# set the cache name specific to imagefit with the cache dict
IMAGEFIT_CACHE_BACKEND_NAME = 'imagefit'
CACHES = {

    'default':

        {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'KEY_PREFIX': 'DNigne.Productsion',  # Change this
            'LOCATION': '127.0.0.1:11211',
            'TIMEOUT': 24 * 3600

        },
    'imagefit': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(tempfile.gettempdir(), 'django_imagefit')
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }

}
SELECT2_CACHE_BACKEND = "select2"
IMAGEFIT_PRESETS = {
    'thumbnail': {'width': 64, 'height': 64, 'crop': True},
    'my_preset1': {'width': 300, 'height': 220},
    'my_preset2': {'width': 100},
}
# ...


####################################
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
# SESSION_COOKIE_SECURE = True
# LOGIN_URL = '/admin/login'
# LOGOUT_URL = '/admin/logout'
# LOGIN_REDIRECT_URL = '/login'
# Cart
CART_SESSION_ID = 'cart'
SESSION_COOKIE_AGE = 85555
SESSION_COOKIE_SECURE = False
AUTH_USER_MODEL = 'user.User'
ROOT_URLCONF = 'DNigne.urls'
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

############Payment STRIPE########
STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = env('STRIPE_WEBHOOK_SECRET')


django_heroku.settings(locals())
DISABLE_COLLECTSTATIC=1