from django.db import models
from users.models import NormalUserInfo
from consultants.models import ConsultantService
from phishing.models import PhishingAttackSimulation
# Create your models here.
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        # Add more payment methods as needed
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('initiated', 'Initiated'),  # Add initiated status if necessary
        ('paid', 'Paid'),
    ]

    user = models.ForeignKey(NormalUserInfo, on_delete=models.CASCADE, related_name='payments')
    consultant_service = models.ForeignKey(ConsultantService, on_delete=models.CASCADE, null=True, blank=True, related_name='payments')
    phishing_simulation_service = models.ForeignKey(PhishingAttackSimulation, on_delete=models.CASCADE, null=True, blank=True, related_name='payments')
    amount = models.IntegerField()  # Amount in the smallest currency unit (e.g., cents)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=255, unique=True)  # ID from the payment gateway
    reference_number = models.CharField(max_length=255, unique=True, blank=True, null=True)  # Unique reference number
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_url = models.URLField(max_length=255, blank=True, null=True)  # URL for transaction authorization
    gateway_id = models.CharField(max_length=255, blank=True, null=True)  # Gateway-specific ID

    def __str__(self):
        return f"Payment {self.reference_number} by {self.user.user.username} - Status: {self.payment_status}"