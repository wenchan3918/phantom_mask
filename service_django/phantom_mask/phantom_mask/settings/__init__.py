import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'SECRET_KEY')

SITE_URL = os.getenv('SITE_URL', 'SITE_URL')

DEBUG = os.getenv('DEBUG', '1') == '1'

if DEBUG:
    from dotenv import load_dotenv

    env_path = os.path.join(BASE_DIR, '../../', '.env')
    if not os.path.isfile(env_path):
        print("\033[91m=====.env file not exists.====\033[97m")
        # exit()
    else:
        print("\033[92m=====.env file loaded.====\033[97m")
        load_dotenv(dotenv_path=env_path)

from .silk import *
from .database import *
from .installed_apps import *
from .rest_framework import *


ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', "127.0.0.1,localhost").split(',')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# print("==os.getenv('ENABLE_SILK', '0')", os.getenv('ENABLE_SILK', "0"))
if os.getenv('ENABLE_SILK', "0") == "1":
    index = 0
    for i, w in enumerate(MIDDLEWARE):
        if not w.startswith('corsheaders.') and not w.startswith('django.'):
            index = i
            break
    MIDDLEWARE = MIDDLEWARE[0:index] + ['silk.middleware.SilkyMiddleware'] + MIDDLEWARE[index:]
    # print(MIDDLEWARE)

ROOT_URLCONF = 'phantom_mask.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'phantom_mask.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = False

USE_TZ = False  # 必須為False,這樣才不會有8小時時差

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
# print("===STATICFILES_DIRS", STATICFILES_DIRS)
# STATICFILES_DIRS = [  # python manage.py collectstatic 則會將下方覆蓋到STATIC_ROOT
#     # os.path.join(BASE_DIR, 'core/static'),
# ]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'compressor.finders.CompressorFinder',
)



MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
