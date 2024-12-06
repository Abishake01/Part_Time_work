from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    USER_ROLES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('admin', 'Admin'),
        ('agent', 'Agent'),
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default='customer')

    # Resolve reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Unique related_name to avoid conflicts
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Unique related_name to avoid conflicts
        blank=True,
    )
# Customer Models
class Product(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='products/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    date_added = models.DateField(auto_now_add=True)

class Order(models.Model):
    STATUS_CHOICES = (
        ('delivered', 'Delivered'),
        ('in_progress', 'In Progress'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    pay_status = models.BooleanField(default=False)
    delivery_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    date = models.DateField(auto_now_add=True)

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    start_date = models.DateField()
    end_date = models.DateField()
    vacation_dates = models.TextField(help_text="Dates to skip delivery ")

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    low_balance_notification = models.BooleanField(default=False)

# Vendor Models
class VendorItem(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_items')
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='vendor_items/')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('payment_pending', 'Payment Pending'),
        ('paid', 'Paid'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    date_uploaded = models.DateTimeField(auto_now_add=True)

# Admin Models
class Agent(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agents')
    name = models.CharField(max_length=255)
    history = models.TextField(help_text="Agent history (date-wise)", blank=True, null=True)

class AdminOrderHistory(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_order_history')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_status = models.CharField(max_length=20)

class VendorPaymentPending(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor_payment_pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

# Agent Models
class AgentOrder(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agent_orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_quantity_taken = models.PositiveIntegerField()
    selled_quantity = models.PositiveIntegerField()
    returned_quantity = models.PositiveIntegerField()
    returned_amount = models.DecimalField(max_digits=10, decimal_places=2)
    history = models.TextField(help_text="Agent's own history", blank=True, null=True)

# Profile and Transactions
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    personal_details = models.TextField()
    language = models.CharField(max_length=50)
    delivery_preferences = models.TextField()
    contact_us = models.TextField()

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
