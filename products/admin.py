from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Basic admin to avoid super() attribute errors"""
    list_display = ['name', 'store', 'category', 'price', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'store__name']
    ordering = ['-created_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Basic admin to avoid super() attribute errors"""
    list_display = ['name', 'icon', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
