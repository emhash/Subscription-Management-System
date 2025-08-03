from .base import *
import os

DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')


# ============  MySQL Setup(can be set postgresql as well) ======================
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('DB_USER', default=''),
        'PASSWORD': os.environ.get('DB_PASSWORD', default=''),
        'HOST': os.environ.get('DB_HOST', default=''),
        'PORT': os.environ.get('DB_PORT', default=''),
    }
}


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR.parent / 'staticfiles'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR.parent / 'mediafiles'


# ============ Production Celery Settings ============>>
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_EAGER_PROPAGATES = False

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_CONNECTION_RETRY = True
CELERY_BROKER_CONNECTION_MAX_RETRIES = 10


# Security settings for production ====>>
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'



# Production logging configuration ====>>
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR.parent / 'logs' / 'django_error.log',
            'formatter': 'verbose',
        },
        'celery_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR.parent / 'logs' / 'celery.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'ERROR',
    },
    'loggers': {
        'celery': {
            'handlers': ['celery_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps.subscription.tasks': {
            'handlers': ['celery_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


print("################ PRODUCTION SETTINGS ###############")