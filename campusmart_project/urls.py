"""
URL configuration for campusmart_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from . import views
from . import api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Notifications
    path('notifications/', include('notifications.urls')),
    
    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    
    # Accounts
    path('accounts/', include('accounts.urls')),
    
    # Stores
    path('stores/', include('stores.urls')),
    
    # Products
    path('products/', include('products.urls')),
    path('product/<int:pk>/', views.product_detail_redirect, name='product_detail'),
    
    # Orders
    path('orders/', include('orders.urls')),
    
    # Chat
    path('chat/', include('chat.urls')),
    
    # API endpoints for favorites
    path('api/add-to-favorites/<int:product_id>/', api_views.add_to_favorites, name='add_to_favorites'),
    path('api/remove-from-favorites/<int:product_id>/', api_views.remove_from_favorites, name='remove_from_favorites'),
    path('api/add-to-cart/<int:product_id>/', api_views.add_to_cart_api, name='add_to_cart_api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
