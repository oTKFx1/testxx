from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Hashed
    username = models.CharField(max_length=50, unique=True)
    role = models.CharField(
        max_length=50, 
        choices=[
            ('User', 'User'), 
            ('Specialist', 'Specialist'), 
            ('Company', 'Company')  # Added Company option
        ]
    )
    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.pk:  # Only hash the password if creating a new user
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.email})"

class NormalUserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='additional_info')  # FK to User
    phone_number = models.CharField(max_length=20, unique=True)
    token = models.CharField(max_length=255, blank=True, null=True)  # Optional field
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set on update

    def __str__(self):
        return f"{self.user.username} - {self.token}"
    

class SpecialistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='specialist_profile')  # FK to User
    picture = models.ImageField(upload_to='specialist_pictures/', blank=True, null=True)  # Store profile pictures
    description = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True)
    experience_years = models.CharField(max_length=10, blank=True, null=True)
    certificate = models.FileField(upload_to='specialist_certificates/', blank=True, null=True)  # Updated to FileField
    online = models.BooleanField(default=False)
    token = models.CharField(max_length=255, blank=True, null=True)  # Optional field
    average_rating = models.FloatField(default=1.0)  # Default to 1.0
    rating_count = models.IntegerField(default=0)  # Default to 0
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set on update

    def __str__(self):
        return f"{self.user.username} - {self.token}"
    
class Specialization(models.Model):
    specialist = models.ForeignKey(SpecialistProfile, on_delete=models.CASCADE, related_name='specializations')  # FK to SpecialistProfile
    name = models.CharField(max_length=100)  # Field for specialization name

    def __str__(self):
        return self.name


class CyberSecurityCategory(models.Model):
    name = models.CharField(max_length=100)  # Field for category name

    def __str__(self):
        return self.name
    
    