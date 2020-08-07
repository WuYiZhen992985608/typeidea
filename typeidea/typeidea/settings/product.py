from .base import * # NOQA

DEBUG = False
# ALLOWED_HOSTS = ['wuyizhen.com']


DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea_db',
        'USER':'debian-sys-maint',
        'PASSWORD':'123',
        'HOST':'127.0.0.1',
        'PORT':3306,
        'CONN_MAX_AGE': 5 * 60,
        'OPTIONS':{'charset':'utf8mb4'}
    },
}

ADMINS = MANAGERS = (
    ('姓名','992985608@qq.com'),
)

# EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_SUBJECT_PREFIX = ''
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
STATIC_ROOT = '/home/wuyizhen/venvs/typeidea-env/static_files/'
LOGGING = {
    'version':1,
    'disable_existing_loggers':False,
    'formatters':{
        'default':{
            'fromat':'%(levelname)s %(asctime)s %(modele)s:'
                     '%(funcName)s:%(lineno)d %(message)s'
        },
    },
    'handlers':{
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'fromatter':'default',
        },
        'file':{
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':'/tmp/logs/typeidea.log',
            'formatter':'default',
            'maxBytes':1024*1024,
            'backupCount':5,
        },
    },
    'loggers':{
        '':{
            'handlers':['console'],
            'level':'INFO',
            'propagate':'True',
        },
    }
}


# REDIS_URL = '127.0.0.1:6379:1'
#
# CACHES = {
#     'default':{
#         'BACKEND':'django_redis.cache.RedisCache',
#         'LOCATION':REDIS_URL,
#         'TIMEOUT':300,
#         'OPTIONS':{
#             # 'PASSWORD':'<对应密码>',
#             'CLIENT_CLASS':'django_redis.client.DefaultClient',
#             'PARSER_CLASS':'redis.connection.HiredisParser',
#         },
#         'CONNECTION_POOL_CLASS':'redis.connection.BlockingConnectionPool',
#     }
# }