"""
Django settings for typeidea project.

Generated by 'django-admin startproject' using Django 1.11.29.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd18ma9gsri+2h-ubu3822q*gp=clfsng3h%5(*2!ak8_(3*)9*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['127.0.0.1','localhost','.wuyizhen.top','0.0.0.0:8000','*']


# Application definition

INSTALLED_APPS = [
    'typeidea',
    'blog',
    'config',
    'comment',
    'ckeditor',
    'ckeditor_uploader',
    'dal',
    'dal_select2',
    'xadmin',
    'rest_framework',
    'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]

MIDDLEWARE = [
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'blog.middleware.user_id.UserIDMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'typeidea.urls'

THEME = 'bootstrap'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'themes',THEME,'templates')],
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

WSGI_APPLICATION = 'typeidea.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea_db',
        'USER':'root',
        'PASSWORD':'root',
        'HOST':'47.101.142.220',
        'PORT':3306,
        # 'OPTIONS':{'charset':'utf8mb4'}
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT= os.path.join(BASE_DIR,"staticfile")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'themes',THEME,"static"),
]

XADMIN_TITLE = 'Typeidea管理后台'
XADMIN_FOOTER_TITLE = 'power by wuyizhen.com'

CKEDITOR_CONFIGS = {
    'default':{
        'toolbar':'full',
        'height':300,
        'width':800,
        'tabSpaces':4,
        'extraPlugins':'codesnippet',
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'themes','bootstrap','static','media')
# MEDIA_ROOT = MEDIA_URL
CKEDITOR_UPLOAD_PATH = "article_images"
DEFAULT_FILE_STORAGE = 'typeidea.storage.WatermarkStorage'
# USE_MARKDOWN_EDITOR = True

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE':2,
}

# CACHES = {
#     'default':{
#         # 内存缓存
#         'BACKEND':'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION':'unique-snowflake',
#         # 文件缓存
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': '/var/tmp/django_cache',
#         # 数据库缓存
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'my_cache_table',
#         # django推荐分布式缓存系统
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': [
#             '172.19.26.240:11211',
#             '172.19.26.242:11211',
#         ]
#     }
# }
