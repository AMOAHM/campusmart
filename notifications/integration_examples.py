"""
Example integration of notifications with existing views and models.

This file shows how to integrate the notification system into your existing code.
"""

# Example 1: In your user registration view
def create_entrepreneur_view(request):
    """Example of how to send admin notification when new entrepreneur registers"""
    from django.contrib.auth import get_user_model
    from .utils import notify_new_entrepreneur
    
    User = get_user_model()
    
    # Your existing user creation logic
    if request.method == 'POST':
        # Create user
        user = User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password']
        )
        
        # Add entrepreneur role/profile
        # ... your existing logic ...
        
        # Send notification to admins
        notify_new_entrepreneur(user)
        
        return redirect('success')


# Example 2: In your order creation view
def create_order_view(request):
    """Example of how to send notification to entrepreneur when order is placed"""
    from .utils import notify_new_order
    
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            # ... your order fields ...
            entrepreneur=request.POST['entrepreneur'],
            total_amount=request.POST['total_amount']
        )
        
        # Send notification to entrepreneur
        notify_new_order(
            entrepreneur_user=order.entrepreneur.user,
            order_id=order.id,
            total_amount=order.total_amount
        )
        
        return redirect('order_success')


# Example 3: In your order status update view
def update_order_status_view(request, order_id):
    """Example of how to send notification to customer when order status changes"""
    from .utils import notify_order_status_update
    
    order = Order.objects.get(id=order_id)
    
    if request.method == 'POST':
        old_status = order.status
        new_status = request.POST['status']
        
        # Update order status
        order.status = new_status
        order.save()
        
        # Send notification to customer
        notify_order_status_update(
            customer_user=order.customer,
            order_id=order.id,
            status=new_status
        )
        
        return redirect('order_detail', order_id=order_id)


# Example 4: Signal-based integration
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .utils import notify_new_entrepreneur

User = get_user_model()

@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    """Send notification when new user is created with entrepreneur role"""
    if created:
        # Check if user has entrepreneur profile (adjust based on your user model)
        if hasattr(instance, 'entrepreneur_profile'):
            notify_new_entrepreneur(instance)


# Example 5: Model-based integration
class Order(models.Model):
    # ... your existing fields ...
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Send notification to entrepreneur for new order
            from .utils import notify_new_order
            notify_new_order(
                entrepreneur_user=self.entrepreneur.user,
                order_id=self.id,
                total_amount=self.total_amount
            )


# Example 6: Admin integration
from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        if not change:  # New order
            from .utils import notify_new_order
            notify_new_order(
                entrepreneur_user=obj.entrepreneur.user,
                order_id=obj.id,
                total_amount=obj.total_amount
            )


# Example 7: API integration
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import notify_new_order

class CreateOrderAPI(APIView):
    def post(self, request):
        # Create order logic
        order = Order.objects.create(**request.data)
        
        # Send notification
        notify_new_order(
            entrepreneur_user=order.entrepreneur.user,
            order_id=order.id,
            total_amount=order.total_amount
        )
        
        return Response({'status': 'success', 'order_id': order.id})
