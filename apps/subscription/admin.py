from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Plan, Subscription, ExchangeRateLog

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_display', 'duration_days', 'subscription_count', 'created_at']
    list_filter = ['duration_days', 'created_at']
    search_fields = ['name']
    ordering = ['price']
    readonly_fields = ['created_at', 'updated_at']
    
    def price_display(self, obj):
        return f"${obj.price}"
    price_display.short_description = "Price"
    
    def subscription_count(self, obj):
        count = obj.subscriptions.count()
        if count > 0:
            url = reverse('admin:subscription_subscription_changelist')
            return format_html(
                '<a href="{}?plan__id={}">{} subscriptions</a>',
                url, obj.id, count
            )
        return "0 subscriptions"
    subscription_count.short_description = "Subscriptions"

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user_display', 'plan', 'start_date', 'end_date', 'status_display', 'days_remaining', 'created_at']
    list_filter = ['status', 'plan', 'created_at', 'start_date', 'end_date']
    search_fields = ['user__username', 'user__email', 'plan__name']
    readonly_fields = ['created_at', 'updated_at', 'days_remaining_display']
    date_hierarchy = 'created_at'
    actions = ['cancel_subscriptions', 'activate_subscriptions']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'plan')
    
    def user_display(self, obj):
        return f"{obj.user.username} ({obj.user.email})"
    user_display.short_description = "User"
    
    def status_display(self, obj):
        colors = {
            'active': 'green',
            'cancelled': 'orange', 
            'expired': 'red'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    status_display.short_description = "Status"
    
    def days_remaining(self, obj):
        if obj.status != 'active':
            return '-'
        from django.utils import timezone
        remaining = (obj.end_date - timezone.now()).days
        return max(0, remaining)
    days_remaining.short_description = "Days Left"
    
    def days_remaining_display(self, obj):
        return self.days_remaining(obj)
    days_remaining_display.short_description = "Days Remaining"
    
    def cancel_subscriptions(self, request, queryset):
        updated = queryset.filter(status='active').update(status='cancelled')
        self.message_user(request, f'{updated} subscriptions cancelled.')
    cancel_subscriptions.short_description = "Cancel selected subscriptions"
    
    def activate_subscriptions(self, request, queryset):
        updated = queryset.filter(status__in=['cancelled', 'expired']).update(status='active')
        self.message_user(request, f'{updated} subscriptions activated.')
    activate_subscriptions.short_description = "Activate selected subscriptions"

@admin.register(ExchangeRateLog)
class ExchangeRateLogAdmin(admin.ModelAdmin):
    list_display = ['currency_pair', 'rate', 'fetched_at']
    list_filter = ['base_currency', 'target_currency', 'fetched_at']
    search_fields = ['base_currency', 'target_currency']
    readonly_fields = ['fetched_at']
    date_hierarchy = 'fetched_at'
    ordering = ['-fetched_at']
    
    def currency_pair(self, obj):
        return f"{obj.base_currency}/{obj.target_currency}"
    currency_pair.short_description = "Currency Pair"
