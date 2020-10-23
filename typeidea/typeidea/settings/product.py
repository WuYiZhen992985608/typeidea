from .base import * # NOQA

DEBUG = False
ALLOWED_HOSTS = ['*']


DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'typeidea_db',
        'NAME': 'typeidea_db1',
        'USER':'root',
        'PASSWORD':'root',
        'HOST':'47.101.142.220',
        'PORT':3306,
        # 'CONN_MAX_AGE': 5 * 60,
        'OPTIONS':{'charset':'utf8mb4'}
    },
}
STATIC_ROOT= os.path.join(BASE_DIR,"staticfile")


# REDIS_URL = '127.0.0.1:6379:1'


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
