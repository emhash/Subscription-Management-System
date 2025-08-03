from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from ..models import Plan, Subscription, ExchangeRateLog
from ..serializers import (
    PlanSerializer, SubscriptionSerializer, CreateSubscriptionSerializer,
    CancelSubscriptionSerializer, ExchangeRateRequestSerializer,
    ExchangeRateResponseSerializer, ExchangeRateLogSerializer
)
from ..utils import convert_usd_to_bdt


class SubscribeAPIView(CreateAPIView):
    serializer_class = CreateSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Subscribe to a plan",
        description="Create a new subscription for the authenticated user",
        responses={
            201: SubscriptionSerializer,
            400: "Bad Request - Validation errors",
            401: "Unauthorized - Invalid or missing JWT token"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    subscription = serializer.save()
                    response_serializer = SubscriptionSerializer(subscription)
                    
                    return Response({
                        'message': 'Subscription created successfully',
                        'data': response_serializer.data
                    }, status=status.HTTP_201_CREATED)
                    
            except Exception as e:
                return Response({
                    'message': f'Failed to create subscription: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'message': 'Validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserSubscriptionsAPIView(ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Subscription.objects.filter(
            user=self.request.user
        ).select_related('plan', 'user').order_by('-created_at')
    
    @extend_schema(
        summary="Get user's subscriptions",
        description="List all subscriptions for the authenticated user",
        responses={
            200: SubscriptionSerializer(many=True),
            401: "Unauthorized - Invalid or missing JWT token"
        }
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'message': 'Subscriptions retrieved successfully',
            'count': queryset.count(),
            'data': serializer.data
        })


class CancelSubscriptionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Cancel subscription",
        description="Cancel an active subscription for the authenticated user",
        request=CancelSubscriptionSerializer,
        responses={
            200: SubscriptionSerializer,
            400: "Bad Request - Validation errors",
            401: "Unauthorized - Invalid or missing JWT token",
            404: "Not Found - Subscription not found"
        }
    )
    def post(self, request):
        serializer = CancelSubscriptionSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    subscription = serializer.save()
                    response_serializer = SubscriptionSerializer(subscription)
                    
                    return Response({
                        'message': 'Subscription cancelled successfully',
                        'data': response_serializer.data
                    })
                    
            except Exception as e:
                return Response({
                    'message': f'Failed to cancel subscription: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'message': 'Validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ExchangeRateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Get exchange rate",
        description="Fetch current exchange rate and store in log",
        parameters=[
            OpenApiParameter(
                name='base',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Base currency code (default: USD)',
                default='USD'
            ),
            OpenApiParameter(
                name='target',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Target currency code (default: BDT)',
                default='BDT'
            ),
        ],
        responses={
            200: ExchangeRateResponseSerializer,
            400: "Bad Request - Invalid currency codes",
            401: "Unauthorized - Invalid or missing JWT token",
            503: "Service Unavailable - External API error"
        }
    )
    def get(self, request):
        serializer = ExchangeRateRequestSerializer(data=request.query_params)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Invalid parameters',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        base_currency = serializer.validated_data['base']
        target_currency = serializer.validated_data['target']
        
        try:
            if base_currency == 'USD' and target_currency == 'BDT':
                result = convert_usd_to_bdt(1.0)
                
                if result is None:
                    return Response({
                        'success': False,
                        'message': 'Failed to fetch exchange rate from external API'
                    }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
                
                bdt_amount, rate = result
                
                log_entry = ExchangeRateLog.objects.create(
                    base_currency=base_currency,
                    target_currency=target_currency,
                    rate=rate
                )
                
                response_data = {
                    'base_currency': base_currency,
                    'target_currency': target_currency,
                    'rate': rate,
                    'fetched_at': log_entry.fetched_at,
                    'message': 'Exchange rate fetched successfully'
                }
                
                return Response({
                    'message': 'Exchange rate retrieved successfully',
                    'data': response_data
                })
            
            else:
                return Response({
                    'message': f'Currency pair {base_currency}/{target_currency} not supported yet'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'message': f'Error fetching exchange rate: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlansListAPIView(ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Get available plans",
        description="List all subscription plans available for purchase",
        responses={
            200: PlanSerializer(many=True),
            401: "Unauthorized - Invalid or missing JWT token"
        }
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'message': 'Plans retrieved successfully',
            'count': queryset.count(),
            'data': serializer.data
        })


class ExchangeRateHistoryAPIView(ListAPIView):
    serializer_class = ExchangeRateLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        base = self.request.query_params.get('base', 'USD')
        target = self.request.query_params.get('target', 'BDT')
        
        return ExchangeRateLog.objects.filter(
            base_currency=base.upper(),
            target_currency=target.upper()
        ).order_by('-fetched_at')[:10]  # Last 10 entries
    
    @extend_schema(
        summary="Get exchange rate history",
        description="Get historical exchange rate data",
        parameters=[
            OpenApiParameter(
                name='base',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Base currency code (default: USD)',
                default='USD'
            ),
            OpenApiParameter(
                name='target',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Target currency code (default: BDT)',
                default='BDT'
            ),
        ],
        responses={
            200: ExchangeRateLogSerializer(many=True),
            401: "Unauthorized - Invalid or missing JWT token"
        }
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'message': 'Exchange rate history retrieved successfully',
            'count': queryset.count(),
            'data': serializer.data
        })
