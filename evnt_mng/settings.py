import dj_database_url
from decouple import config
from pathlib import Path
import sys


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com','http://127.0.0.1:8000']

INSTALLED_APPS = [
    'django.contrib.admin',
    'user.apps.UserConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'event',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'evnt_mng.urls'

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

WSGI_APPLICATION = 'evnt_mng.wsgi.application'


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME', default =''),
#         'USER': config('DB_USER', default =''),
#         'PASSWORD': config('DB_PASSWORD', default =''),
#         "HOST": config('DB_HOST', default =''),  
#         "PORT": config('DB_PORT', cast=int), 
#     }
# }

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://event_management_db_014m_user:6w5QosmeD6MHq5kOxiAkkwXKf9tLUyYK@dpg-cv7ojdnnoe9s73erlsig-a.oregon-postgres.render.com/event_management_db_014m',
        conn_max_age=600
    )
}




FRONTEND_URL = 'https://event-management-django-sdqd.onrender.com'
BACKEND_URL = 'https://event-management-django-sdqd.onrender.com'




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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'
USE_TZ = True

USE_I18N = True


STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'



PASSWORD_RESET_TIMEOUT = 604800
LOGIN_REDIRECT_URL = 'home' 
AUTH_USER_MODEL = 'user.CustomUser'



STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND=config('EMAIL_BACKEND')
EMAIL_HOST=config('EMAIL_HOST')
EMAIL_USE_TLS=config('EMAIL_USE_TLS',cast=bool)
EMAIL_PORT=config('EMAIL_PORT')
EMAIL_HOST_USER=config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=config('EMAIL_HOST_PASSWORD')