from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    """Extend User with additional fields"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    house_address = models.CharField(max_length=255, blank=True)
    contact_number = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
