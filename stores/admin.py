from django.contrib import admin
from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """Basic admin to avoid super() attribute errors"""
    list_display = ['name', 'entrepreneur', 'location', 'phone_number', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description', 'entrepreneur__username', 'location']
    ordering = ['-created_at']
