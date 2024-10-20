from django.db import models
from users.models import User, NormalUserInfo, SpecialistProfile 
# Create your models here.

class ConsultantService(models.Model):
    user = models.ForeignKey(NormalUserInfo, on_delete=models.CASCADE, related_name='consultant_services')  # FK to User
    details = models.TextField(blank=True, null=True)  # Use TextField for longer details
    specialist = models.ForeignKey(SpecialistProfile, on_delete=models.CASCADE, related_name='consultant_services')  # FK to SpecialistProfile
    order_status = models.CharField(
        max_length=20,
        choices=[
            ('waiting_payment', 'Waiting For Payment'),
            ('on_going', 'On Going'),
            ('completed', 'Completed'),
        ],
        default='waiting_payment'  # Default status
    )
    reference_number = models.CharField(max_length=255, unique=True, null=True, blank=True)  # Unique reference number
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set on update

    def __str__(self):
        return f"Service {self.reference_number} for {self.user.user.username}"
    
class ConsultantDocument(models.Model):
    service = models.ForeignKey(ConsultantService, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='consultant_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for Service {self.service.reference_number}"
    
class ConsultantChat(models.Model):
    consultant = models.ForeignKey(ConsultantService, on_delete=models.CASCADE, related_name='chats')  # FK to ConsultantService
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')  # FK to User
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')  # FK to User
    message = models.TextField(blank=True, null=True)  # Text message content
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)  # Store files (images, videos, etc.)
    read = models.BooleanField(default=False)  # Indicates if the message has been read
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set on update

    def __str__(self):
        return f"Chat from {self.from_user.username} to {self.to_user.username}"
    

class Report(models.Model):
    user = models.ForeignKey(NormalUserInfo, on_delete=models.CASCADE)
    consultant_service = models.ForeignKey(ConsultantService, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.user.user.username} on {self.consultant_service.id}"