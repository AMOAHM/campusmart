from django.db import models
from accounts.models import User
from stores.models import Store


class ChatRoom(models.Model):
    ROOM_TYPE_CHOICES = [
        ('support', 'Support'),
        ('entrepreneur', 'Entrepreneur'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_rooms')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True, related_name='chat_rooms')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='support')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        customer_name = self.customer.username if self.customer else "Unknown Customer"
        if self.room_type == 'support':
            return f"Support Chat with {customer_name}"
        store_name = self.store.name if self.store else "Unknown Store"
        return f"Chat between {customer_name} and {store_name}"


class ChatMessage(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        sender_name = self.sender.username if self.sender else "Deleted User"
        return f"Message from {sender_name} at {self.created_at}"

