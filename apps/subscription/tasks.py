from celery import shared_task
from django.utils import timezone
from .utils import convert_usd_to_bdt
from .models import ExchangeRateLog, Subscription

import logging

logger = logging.getLogger(__name__)

@shared_task
def fetch_exchange_rate(base_currency='USD', target_currency='BDT'):
    logger.info(f"Starting exchange rate fetch task: {base_currency} to {target_currency}")
    
    try:
        if base_currency == 'USD' and target_currency == 'BDT':
            result = convert_usd_to_bdt(1.0)
            
            if result is None:
                logger.error("Failed to fetch exchange rate from external API")
                return {
                    'status': 'error',
                    'message': 'Failed to fetch exchange rate from external API'
                }
            
            bdt_amount, rate = result
            
            log_entry = ExchangeRateLog.objects.create(
                base_currency=base_currency,
                target_currency=target_currency,
                rate=rate
            )
            
            logger.info(f"Successfully fetched and saved exchange rate: {base_currency}/{target_currency} = {rate}")
            
            return {
                'status': 'success',
                'message': f"Exchange rate fetched and saved: {base_currency}/{target_currency} = {rate}",
                'rate': str(rate),
                'log_id': log_entry.id,
                'fetched_at': log_entry.fetched_at.isoformat()
            }
        
        else:
            logger.warning(f"Currency pair {base_currency}/{target_currency} not supported")
            return {
                'status': 'error',
                'message': f'Currency pair {base_currency}/{target_currency} not supported yet'
            }
            
    except Exception as e:
        logger.error(f"Error in fetch_exchange_rate task: {str(e)}")
        return {
            'status': 'error',
            'message': f'Error fetching exchange rate: {str(e)}'
        }

@shared_task
def update_expired_subscriptions():
    logger.info("Starting expired subscriptions update task")
    
    try:
        expired_subscriptions = Subscription.objects.filter(
            status='active',
            end_date__lt=timezone.now()
        )
        
        count = expired_subscriptions.update(status='expired')
        
        logger.info(f"Updated {count} expired subscriptions")
        
        return {
            'status': 'success',
            'message': f"Updated {count} expired subscriptions",
            'updated_count': count
        }
        
    except Exception as e:
        logger.error(f"Error in update_expired_subscriptions task: {str(e)}")
        return {
            'status': 'error',
            'message': f'Error updating expired subscriptions: {str(e)}'
        }

@shared_task
def periodic_exchange_rate_fetch():
    logger.info("Starting periodic exchange rate fetch task")
    
    try:
        result = fetch_exchange_rate.delay('USD', 'BDT')
        task_result = result.get()
        
        logger.info(f"Periodic exchange rate fetch completed: {task_result}")
        
        return {
            'status': 'success',
            'message': 'Periodic exchange rate fetch completed',
            'task_result': task_result
        }
        
    except Exception as e:
        logger.error(f"Error in periodic_exchange_rate_fetch: {str(e)}")
        return {
            'status': 'error',
            'message': f'Error in periodic exchange rate fetch: {str(e)}'
        }