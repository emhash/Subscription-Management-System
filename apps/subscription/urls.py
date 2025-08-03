from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views.api_view import (
    SubscribeAPIView, UserSubscriptionsAPIView, CancelSubscriptionAPIView,
    ExchangeRateAPIView, PlansListAPIView, ExchangeRateHistoryAPIView
)
from .views.mvt_view import subscription_list

urlpatterns = [
    path('subscribe/', SubscribeAPIView.as_view(), name='api_subscribe'),
    path('subscriptions/', UserSubscriptionsAPIView.as_view(), name='api_user_subscriptions'),
    path('cancel/', CancelSubscriptionAPIView.as_view(), name='api_cancel_subscription'),
    path('exchange-rate/', ExchangeRateAPIView.as_view(), name='api_exchange_rate'),
    
    path('plans/', PlansListAPIView.as_view(), name='api_plans_list'),
    path('exchange-rate/history/', ExchangeRateHistoryAPIView.as_view(), name='api_exchange_rate_history'),
    
    path('auth/login/', TokenObtainPairView.as_view(), name='api_token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    
    # for frontend - MVT
    path('', subscription_list, name='subscription-list'),
]
