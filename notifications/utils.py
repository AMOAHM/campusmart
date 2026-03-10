from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

def notify_new_entrepreneur(user):
    """
    Send notification to all admins when a new entrepreneur registers
    Call this function when a new entrepreneur is created
    """
    title = "New Entrepreneur Registration"
    message = f"{user.username} has registered as a new entrepreneur on the platform."
    
    # Get all admin users
    admins = User.objects.filter(is_staff=True)
    
    # Create notification for each admin
    notifications = []
    for admin in admins:
        notifications.append(Notification(
            recipient=admin,
            notification_type='new_entrepreneur',
            title=title,
            message=message,
            entrepreneur_id=user.id
        ))
    
    # Bulk create notifications
    Notification.objects.bulk_create(notifications)

def notify_new_order(entrepreneur_user, order_id, total_amount):
    """
    Send notification to entrepreneur when they receive a new order
    Call this function when a new order is placed
    """
    title = "New Order Received"
    message = f"You have received a new order (Order #{order_id}). Total: ${total_amount}"
    
    Notification.create_notification(
        recipient=entrepreneur_user,
        notification_type='new_order',
        title=title,
        message=message,
        order_id=order_id
    )

def notify_order_status_update(customer_user, order_id, status):
    """
    Send notification to customer when order status changes
    Call this function when order status is updated
    """
    title = "Order Status Updated"
    message = f"Your order #{order_id} status has been updated to: {status}"
    
    Notification.create_notification(
        recipient=customer_user,
        notification_type='order_status',
        title=title,
        message=message,
        order_id=order_id
    )
