from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save
import random


class Dashboard (models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    balance = models.CharField(max_length=200, blank=True, null=True)
    wallet_id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False)
    budget = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    otp = models.IntegerField(blank=True, null=True)
    is_verified = models.IntegerField(default=False)
    monthly_capital = models.CharField(max_length=200, blank=True, null=True)
    income = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.wallet_id)


class Cards (models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    card_number = models.CharField(max_length=200, blank=True, null=True)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    balance = models.CharField(max_length=200, blank=True, null=True)
    revenue = models.CharField(max_length=200, blank=True, null=True)
    spent = models.CharField(max_length=200, blank=True, null=True)
    expires_at = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    def __str__(self):
        return str(self.card_number)


class Reminder (models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    balance = models.CharField(max_length=200, blank=True, null=True)
    is_paid = models.IntegerField(default=False)
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    tags = models.CharField(max_length=200, blank=True, null=True)
    is_autopay = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    def __str__(self):
        return str(self.name)


class Transactions (models.Model):
    type = models.CharField(max_length=200, blank=True, null=True)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=200, blank=True, null=True)
    reciver = models.CharField(max_length=200, blank=True, null=True)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    def __str__(self):
        return str(self.transaction_id)
