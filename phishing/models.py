from django.db import models
from users.models import NormalUserInfo  # Adjust the import based on your actual user model

class PhishingAttackSimulation(models.Model):
    user = models.ForeignKey(NormalUserInfo, on_delete=models.CASCADE)  # FK to User
    company_name = models.CharField(max_length=100)
    company_website = models.CharField(max_length=100, null=True, blank=True)
    company_industry = models.CharField(max_length=100, null=True, blank=True)
    user_list = models.FileField(upload_to='user_lists/')  # Store the CSV file
    total_users = models.IntegerField(null=True, blank=True)
    order_status = models.CharField(
        max_length=20,
        choices=[
            ('waiting_payment', 'Waiting For Payment'),
            ('on_going', 'On Going'),
            ('completed', 'Completed'),
        ],
        default='waiting_payment'  # Default status
    )
    reference_number = models.CharField(max_length=255, unique=True, blank=True, null=True)  # Unique reference number
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation

    def __str__(self):
        return f"Phishing Simulation for {self.company_name} (Ref: {self.reference_number})"