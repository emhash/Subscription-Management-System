from django.core.management.base import BaseCommand
from apps.subscription.tasks import fetch_exchange_rate, update_expired_subscriptions


class Command(BaseCommand):
    help = 'Test Celery tasks for subscription management'

    def add_arguments(self, parser):
        parser.add_argument(
            '--task',
            type=str,
            choices=['exchange', 'subscriptions', 'all'],
            default='all',
            help='Which task to test (exchange, subscriptions, or all)',
        )
        parser.add_argument(
            '--async',
            action='store_true',
            help='Run tasks asynchronously (requires Redis/broker)',
        )

    def handle(self, *args, **options):
        task_type = options['task']
        run_async = options['async']

        self.stdout.write(
            self.style.SUCCESS(f'Testing Celery tasks (async={run_async})...')
        )

        if task_type in ['exchange', 'all']:
            self.test_exchange_rate_task(run_async)

        if task_type in ['subscriptions', 'all']:
            self.test_subscription_task(run_async)

        self.stdout.write(
            self.style.SUCCESS('Celery task tests completed!')
        )

    def test_exchange_rate_task(self, run_async):
        self.stdout.write('Testing exchange rate fetch task...')
        
        try:
            if run_async:
                result = fetch_exchange_rate.delay('USD', 'BDT')
                self.stdout.write(f'Task submitted with ID: {result.id}')
                
                task_result = result.get(timeout=30)
                self.stdout.write(f'Task result: {task_result}')
            else:
                result = fetch_exchange_rate('USD', 'BDT')
                self.stdout.write(f'Task result: {result}')
                
            self.stdout.write(
                self.style.SUCCESS('[OK] Exchange rate task completed successfully')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'[NOT] Exchange rate task failed: {str(e)}')
            )

    def test_subscription_task(self, run_async):
        self.stdout.write('Testing subscription update task...')
        
        try:
            if run_async:
                result = update_expired_subscriptions.delay()
                self.stdout.write(f'Task submitted with ID: {result.id}')
                
                # Wait for result (optional)
                task_result = result.get(timeout=30)
                self.stdout.write(f'Task result: {task_result}')
            else:
                result = update_expired_subscriptions()
                self.stdout.write(f'Task result: {result}')
                
            self.stdout.write(
                self.style.SUCCESS('[OK] Subscription task completed successfully')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'[NOT] Subscription task failed: {str(e)}')
            )