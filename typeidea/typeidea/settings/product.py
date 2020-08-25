from .base import * # NOQA

DEBUG = False
# ALLOWED_HOSTS = ['wuyizhen.com']


DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea_db',
        'USER':'root',
        'PASSWORD':'root',
        'HOST':'47.101.142.220',
        'PORT':3306,
        'CONN_MAX_AGE': 5 * 60,
        'OPTIONS':{'charset':'utf8mb4'}
    },
}

ADMINS = MANAGERS = (
	('何羿霖','992985608@qq.com'),
)
EMAIL_HOST = 'smtp.qq.com'
EMAIL_HOST_USER = '992985608@qq.com'
EMAIL_HOST_PASSWORD = '029490heyilin'
EMAIL_SUBJECT_PREFIX = 'typeidea_err‘
DEFAULT_FROM_EMAIL = 'TYPEIDEA'
SERVER_EMAIL = 'smtp.qq.com'

STATIC_ROOT = '/var/www/typeidea/typeidea/typeidea/themes/bootstrap/
static'
LOGGING = {
	'version':1,
	'disable_existing_loggers':False,
	'formatters':{
		'default':{
			'format':'%(levelname)s %(asctime)s %(module
			)s:%(funcName)s:%(lineno)d %(message)s'
		},
	},
	'handlers':{
		'console':{
			'level':'INFO',
			'class':'logging.StreamHandler',
			'formatter':'default',
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
			'handlers':{'console'},
			'level':'INFO',
			'propagate':True,
		},
	},
}

