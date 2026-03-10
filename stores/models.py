from django.db import models
from accounts.models import User
from django.utils import timezone


class Store(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    entrepreneur = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='store')
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text='WhatsApp phone number (with country code, e.g., +233XXXXXXXXX)')
    logo = models.ImageField(upload_to='stores/logos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

