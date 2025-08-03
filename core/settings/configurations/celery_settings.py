import os
from kombu import Queue

# ============ Celery Configuration ============>>

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Dhaka'
CELERY_ENABLE_UTC = True

CELERY_TASK_ALWAYS_EAGER = os.environ.get('CELERY_TASK_ALWAYS_EAGER', 'False').lower() in ('true', '1', 't')
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60

CELERY_RESULT_EXPIRES = 3600
CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS = {
    'master_name': 'mymaster',
}

CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000

CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_ACKS_LATE = True

CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_QUEUES = (
    Queue('default', routing_key='default'),
    Queue('exchange_rates', routing_key='exchange_rates'),
    Queue('subscriptions', routing_key='subscriptions'),
)

CELERY_TASK_ROUTES = {
    'apps.subscription.tasks.fetch_exchange_rate': {'queue': 'exchange_rates'},
    'apps.subscription.tasks.periodic_exchange_rate_fetch': {'queue': 'exchange_rates'},
    'apps.subscription.tasks.update_expired_subscriptions': {'queue': 'subscriptions'},
}

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_WORKER_HIJACK_ROOT_LOGGER = False
CELERY_WORKER_LOG_FORMAT = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
CELERY_WORKER_TASK_LOG_FORMAT = '[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s'

# Error handling
CELERY_TASK_ANNOTATIONS = {
    '*': {
        'rate_limit': '100/m',
        'time_limit': 30 * 60,
        'soft_time_limit': 25 * 60,
    },
    'apps.subscription.tasks.fetch_exchange_rate': {
        'rate_limit': '10/m',
    },
} 