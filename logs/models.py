from django.db import models
from accounts.models import User


class SystemLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('store_created', 'Store Created'),
        ('product_added', 'Product Added'),
        ('product_edited', 'Product Edited'),
        ('product_deleted', 'Product Deleted'),
        ('order_placed', 'Order Placed'),
        ('order_status_updated', 'Order Status Updated'),
        ('chat_message', 'Chat Message'),
        ('store_blocked', 'Store Blocked'),
        ('store_deactivated', 'Store Deactivated'),
        ('user_created', 'User Created'),
        ('user_role_changed', 'User Role Changed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='system_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'action']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.get_action_display()} by {self.user.username if self.user else 'Unknown'}"
