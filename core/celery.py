import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('subscription_management')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.update(
    task_track_started=True,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    result_expires=3600,
    timezone='Asia/Dhaka',
    enable_utc=True,
)

# Celery Beat-->>
from celery.schedules import crontab

app.conf.beat_schedule = {
    'fetch-exchange-rate-hourly': {
        'task': 'apps.subscription.tasks.fetch_exchange_rate',
        'schedule': crontab(minute=0),
        'args': ('USD', 'BDT'),
    },
    'update-expired-subscriptions-daily': {
        'task': 'apps.subscription.tasks.update_expired_subscriptions',
        'schedule': crontab(hour=0, minute=0),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 