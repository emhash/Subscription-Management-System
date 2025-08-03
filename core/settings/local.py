from .base import *

DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# print("ALLOWED_HOSTS:", ALLOWED_HOSTS)

import logging
logging.getLogger("django.server").setLevel(logging.ERROR)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ============ Local Celery Settings ============>>
# For development, you can run tasks synchronously or use Redis if available
CELERY_TASK_ALWAYS_EAGER = os.getenv('CELERY_TASK_ALWAYS_EAGER', 'True').lower() in ('true', '1', 't')
CELERY_TASK_EAGER_PROPAGATES = True

# Redis settings for local development (if Redis is running)
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# If Redis is not available, tasks will run synchronously due to CELERY_TASK_ALWAYS_EAGER=True


# Logging configuration for development =====>>
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


print("################ LOCAL SETTINGS ###############")