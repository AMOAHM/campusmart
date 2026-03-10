# Use Django's default admin for User model to avoid all super() attribute issues
from django.contrib import admin
from .models import User

# Register User model with Django's default admin (no custom class)
admin.site.register(User)
