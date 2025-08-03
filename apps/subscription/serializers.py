from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
from .models import Plan, Subscription, ExchangeRateLog


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'duration_days', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    plan = PlanSerializer(read_only=True)
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    plan_price = serializers.DecimalField(source='plan.price', max_digits=10, decimal_places=2, read_only=True)
    days_remaining = serializers.SerializerMethodField()
    is_expired = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Subscription
        fields = [
            'id', 'user', 'plan', 'plan_name', 'plan_price',
            'start_date', 'end_date', 'status', 'days_remaining', 
            'is_expired', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'plan', 'end_date', 'created_at', 'updated_at']
    
    def get_days_remaining(self, obj):
        if obj.status != 'active':
            return 0
        
        remaining = (obj.end_date - timezone.now()).days
        return max(0, remaining)


class CreateSubscriptionSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()
    
    def validate_plan_id(self, value):
        try:
            plan = Plan.objects.get(id=value)
            return value
        except Plan.DoesNotExist:
            raise serializers.ValidationError("Plan not found.")
    
    def validate(self, attrs):
        user = self.context['request'].user
        plan_id = attrs['plan_id']
        
        # checking any active subscription for this plan ==>
        existing_subscription = Subscription.objects.filter(
            user=user,
            plan_id=plan_id,
            status='active'
        ).exists()
        
        if existing_subscription:
            raise serializers.ValidationError(
                "You already have an active subscription for this plan."
            )
        
        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        plan = Plan.objects.get(id=validated_data['plan_id'])
        
        subscription = Subscription.objects.create(
            user=user,
            plan=plan,
            start_date=timezone.now(),
            status='active'
        )
        
        return subscription


class CancelSubscriptionSerializer(serializers.Serializer):
    subscription_id = serializers.IntegerField()
    
    def validate_subscription_id(self, value):
        user = self.context['request'].user
        
        try:
            subscription = Subscription.objects.get(
                id=value,
                user=user,
                status='active'
            )
            return value
        except Subscription.DoesNotExist:
            raise serializers.ValidationError(
                "Active subscription not found or doesn't belong to you."
            )
    
    @transaction.atomic
    def save(self):
        subscription_id = self.validated_data['subscription_id']
        user = self.context['request'].user
        
        subscription = Subscription.objects.get(
            id=subscription_id,
            user=user,
            status='active'
        )
        
        subscription.status = 'cancelled'
        subscription.save()
        
        return subscription


class ExchangeRateLogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExchangeRateLog
        fields = ['id', 'base_currency', 'target_currency', 'rate', 'fetched_at']
        read_only_fields = ['id', 'fetched_at']


class ExchangeRateRequestSerializer(serializers.Serializer):
    base = serializers.CharField(max_length=3, default='USD')
    target = serializers.CharField(max_length=3, default='BDT')
    
    def validate_base(self, value):
        return value.upper()
    
    def validate_target(self, value):
        return value.upper()


class ExchangeRateResponseSerializer(serializers.Serializer):
    base_currency = serializers.CharField()
    target_currency = serializers.CharField()
    rate = serializers.DecimalField(max_digits=15, decimal_places=6)
    fetched_at = serializers.DateTimeField()
    success = serializers.BooleanField()
    message = serializers.CharField(required=False) 