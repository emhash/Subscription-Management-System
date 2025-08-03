import os
import sys
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.subscription.models import Plan, Subscription


class Command(BaseCommand):
    help = "Create sample data for plans, users, and subscriptions"

    def handle(self, *args, **kwargs):
        plans_data = [
            {"name": "Basic Plan", "price": Decimal("9.99"), "duration_days": 30},
            {"name": "Premium Plan", "price": Decimal("19.99"), "duration_days": 30},
            {"name": "Pro Plan", "price": Decimal("29.99"), "duration_days": 30},
            {"name": "Annual Basic", "price": Decimal("99.99"), "duration_days": 365},
            {"name": "Annual Premium", "price": Decimal("199.99"), "duration_days": 365},
        ]

        self.stdout.write("Creating sample plans...")
        for plan_data in plans_data:
            plan, created = Plan.objects.get_or_create(
                name=plan_data["name"],
                defaults=plan_data
            )
            if created:
                self.stdout.write(f"Created plan: {plan.name}")
            else:
                self.stdout.write(f"Plan already exists: {plan.name}")

        users_data = [
            {"username": "example1", "email": "example1@gmail.com", "password": "testpass123"},
            {"username": "example2", "email": "example2@gmail.com", "password": "testpass123"},
            {"username": "example3", "email": "example3@gmail.com", "password": "testpass123"},
        ]

        self.stdout.write("Creating sample users...")
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                defaults={
                    "email": user_data["email"],
                    "first_name": user_data["username"].split("_")[0].title(),
                    "last_name": user_data["username"].split("_")[1].title() if "_" in user_data["username"] else "",
                }
            )
            if created:
                user.set_password(user_data["password"])
                user.save()
                self.stdout.write(f"Created user: {user.username}")
            else:
                self.stdout.write(f"User already exists: {user.username}")

        self.stdout.write("Creating sample subscriptions...")
        users = User.objects.filter(username__in=[u["username"] for u in users_data])
        plans = Plan.objects.all()

        if users.exists() and plans.exists():
            example1 = users.get(username="example1")
            basic_plan = plans.get(name="Basic Plan")
            subscription, created = Subscription.objects.get_or_create(
                user=example1,
                plan=basic_plan,
                defaults={"status": "active"}
            )
            if created:
                self.stdout.write(f"Created subscription: {example1.username} -> {basic_plan.name}")

            example2 = users.get(username="example2")
            premium_plan = plans.get(name="Premium Plan")
            subscription, created = Subscription.objects.get_or_create(
                user=example2,
                plan=premium_plan,
                defaults={"status": "active"}
            )
            if created:
                self.stdout.write(f"Created subscription: {example2.username} -> {premium_plan.name}")

            example3 = users.get(username="example3")
            annual_basic = plans.get(name="Annual Basic")
            subscription, created = Subscription.objects.get_or_create(
                user=example3,
                plan=annual_basic,
                defaults={"status": "cancelled"}
            )
            if created:
                self.stdout.write(f"Created subscription: {example3.username} -> {annual_basic.name}")

        self.stdout.write("Sample data creation completed!")
        self.stdout.write("You can now:")
        self.stdout.write("1. Visit /admin/ to manage data")
        self.stdout.write("2. Visit /subscriptions/ to view the frontend")
        self.stdout.write("3. Use the API endpoints with the created users")
        self.stdout.write("Sample user credentials:")
        for user_data in users_data:
            self.stdout.write(f"  Username: {user_data['username']}, Password: {user_data['password']}")
