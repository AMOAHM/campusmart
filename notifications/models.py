from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('new_entrepreneur', 'New Entrepreneur Registration'),
        ('new_order', 'New Order Received'),
        ('order_status', 'Order Status Update'),
        ('store_approval', 'Store Approval'),
        ('system', 'System Notification'),
    ]
    
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Related object IDs (optional)
    order_id = models.IntegerField(null=True, blank=True)
    entrepreneur_id = models.IntegerField(null=True, blank=True)
    store_id = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
    
    def get_icon_class(self):
        icon_map = {
            'new_entrepreneur': 'user-plus',
            'new_order': 'shopping-cart',
            'order_status': 'truck',
            'store_approval': 'store',
            'system': 'bell',
        }
        return icon_map.get(self.notification_type, 'bell')
    
    @classmethod
    def create_notification(cls, recipient, notification_type, title, message, **kwargs):
        """Create a new notification"""
        return cls.objects.create(
            recipient=recipient,
            notification_type=notification_type,
            title=title,
            message=message,
            **kwargs
        )
    
    @classmethod
    def notify_admins(cls, notification_type, title, message, **kwargs):
        """Send notification to all admin users"""
        admins = User.objects.filter(is_staff=True)
        notifications = []
        for admin in admins:
            notifications.append(cls(
                recipient=admin,
                notification_type=notification_type,
                title=title,
                message=message,
                **kwargs
            ))
        return cls.objects.bulk_create(notifications)

class NotificationPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    order_notifications = models.BooleanField(default=True)
    system_notifications = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - Preferences"
