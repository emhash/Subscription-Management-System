from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta

class Plan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Price in USD",
        validators=[MinValueValidator(0.01)]
    )
    duration_days = models.IntegerField(
        help_text="Duration in days",
        validators=[MinValueValidator(1), MaxValueValidator(3650)]  # Max 10 years
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ${self.price} for {self.duration_days} days"

    class Meta:
        ordering = ['price']

class Subscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.end_date

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} ({self.status})"

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'plan'],
                condition=models.Q(status='active'),
                name='unique_active_user_plan'
            )
        ]

class ExchangeRateLog(models.Model):
    base_currency = models.CharField(max_length=3)
    target_currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=15, decimal_places=6)
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.base_currency}/{self.target_currency}: {self.rate} at {self.fetched_at}"

    class Meta:
        ordering = ['-fetched_at']
        indexes = [
            models.Index(fields=['base_currency', 'target_currency', '-fetched_at']),
        ]
