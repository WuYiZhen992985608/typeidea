from .base import *  # NOQA  此处不许PEP8检测


DEBUG = True

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'typeidea_db',
        'NAME': 'typeidea_db1',
        # 'USER':'root',
        'USER':'debian-sys-maint',
        'PASSWORD':'123',
        # 'PASSWORD':'root',
        'HOST':'127.0.0.1',
        'PORT':3306,
        # 'OPTIONS':{'charset':'utf8mb4'}
    }
}

INSTALLED_APPS += [
    'debug_toolbar',
    # 'pympler',
    # 'debug_toolbar_line_profiler',
    # 'silk',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'silk.middleware.SilkyMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']
DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL':'https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js',
    # 'SHOW_COLLAPSED': True,
    # 'SHOW_TOOLBAR_CALLBACK': lambda x: True,
}
# DEBUG_TOOLBAR_PANELS = [
#     # 'debug_toolbar.panels.versions.VersionsPanel',
#     # 'debug_toolbar.panels.timer.TimerPanel',
#     # 'debug_toolbar.panels.settings.SettingsPanel',
#     # 'debug_toolbar.panels.headers.HeadersPanel',
#     # 'debug_toolbar.panels.request.RequestPanel',
#     # 'debug_toolbar.panels.sql.SQLPanel',
#     # 'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     # 'debug_toolbar.panels.templates.TemplatesPanel',
#     # 'debug_toolbar.panels.cache.CachePanel',
#     # 'debug_toolbar.panels.signals.SignalsPanel',
#     # 'debug_toolbar.panels.logging.LoggingPanel',
#     # 'debug_toolbar.panels.redirects.RedirectsPanel',
#     # 'djdt_flamegraph.FlamegraphPanel',
#     # 'pympler.panels.MemoryPanel',
#     'debug_toolbar_line_profiler.panel.ProfilingPanel',
# ]
