"""
Django settings for django_wx_joyme project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(y@wu*h2eny#u9%w6%+h2i(@)5(l-60&-(3ipo*zxq*my1xull'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']
"""import python modules"""
import sys

sys.path.insert(0, os.path.join(BASE_DIR, 'third-party'))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'xadmin',
    # 'crispy_forms',
    'app',  # app
    'wechat_manage',
    'permissions',
    'django_static'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.middleware.log_middle_ware.log_middleware'  # log_middle_ware
]

ROOT_URLCONF = 'django_wx_joyme.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'template')],
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

WSGI_APPLICATION = 'django_wx_joyme.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_wx_joyme',
        'USER': 'root',
        'PASSWORD': '11119999',
        'HOST': '172.16.78.73',  # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

"""multi static directory"""
"""copy app/static to root path"""
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'node_modules'),
    os.path.join(BASE_DIR, 'upload')

]

"""caches settings"""
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://172.16.78.73:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
"""setting media"""
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')
MEDIA_PATH = '/upload'
MEDIA_URL = '/upload/'

"""home develop settings"""
import os

if os.path.isdir(os.path.join(BASE_DIR, 'django_wx_joyme', 'home_settings')):
    try:
        import home_settings.database

        DATABASES = home_settings.database.DATABASES
        CACHES = home_settings.database.CACHES

    except (ImportError, NameError):
        pass
APP_NAME = 'django_wx_joyme'

import custome_settings

if os.path.isfile(os.path.join(BASE_DIR, 'is_server')):
    CACHES['default']['LOCATION'] = "redis://127.0.0.1:6379/1"
    DATABASES['default']['HOST'] = 'http://127.0.0.1'
    DATABASES['default']['USER'] = 'django_wx'
    DATABASES['default']['PASSWORD'] = '055b6527a0'
