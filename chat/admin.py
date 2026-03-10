from django.contrib import admin
from .models import ChatRoom, ChatMessage


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    """Simplified admin to avoid super() attribute errors"""
    list_display = ['id', 'customer', 'store', 'room_type', 'created_at']
    list_filter = ['room_type', 'created_at']
    search_fields = ['customer__username', 'store__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    # Remove complex fieldsets that cause super() attribute issues
    fields = ('customer', 'store', 'room_type', 'created_at', 'updated_at')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """Simplified admin to avoid super() attribute errors"""
    list_display = ['id', 'chat_room', 'sender', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['message', 'sender__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    # Remove complex fieldsets that cause super() attribute issues
    fields = ('chat_room', 'sender', 'message', 'is_read', 'created_at')
