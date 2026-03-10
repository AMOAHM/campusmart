from django.contrib import admin
from .models import Notification, NotificationPreference


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Simplified admin to avoid super() attribute errors"""
    list_display = ['title', 'recipient', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'recipient__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    # Remove complex fieldsets that cause super() attribute issues
    fields = ('title', 'message', 'notification_type', 'recipient', 'sender', 'is_read', 'order_id', 'entrepreneur_id', 'store_id', 'created_at')


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    """Simplified admin to avoid super() attribute errors"""
    list_display = ['user', 'email_notifications', 'push_notifications', 'order_notifications', 'system_notifications']
    list_filter = ['email_notifications', 'push_notifications', 'order_notifications', 'system_notifications']
    search_fields = ['user__username']
    # Remove complex fieldsets that cause super() attribute issues
    fields = ('user', 'email_notifications', 'push_notifications', 'order_notifications', 'system_notifications')
