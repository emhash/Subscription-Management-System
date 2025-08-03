from django.shortcuts import render
from django.contrib.auth.models import User
from ..models import Subscription

def subscription_list(request):
    subscriptions = Subscription.objects.select_related('user', 'plan').all()
    
    active_subscriptions = subscriptions.filter(status='active')
    cancelled_subscriptions = subscriptions.filter(status='cancelled')
    expired_subscriptions = subscriptions.filter(status='expired')
    
    context = {
        'subscriptions': subscriptions,
        'active_subscriptions': active_subscriptions,
        'cancelled_subscriptions': cancelled_subscriptions,
        'expired_subscriptions': expired_subscriptions,
        'title': 'All Subscriptions'
    }
    
    return render(request, 'subscriptions/subscription_list.html', context)
