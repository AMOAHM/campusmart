from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Notification, NotificationPreference

@login_required
def notification_list(request):
    """Display all notifications for the user"""
    notifications = request.user.notifications.all()
    
    # Pagination
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unread count
    unread_count = request.user.notifications.filter(is_read=False).count()
    
    return render(request, 'notifications/notification_list.html', {
        'notifications': page_obj,
        'unread_count': unread_count,
    })

@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """Mark a specific notification as read"""
    try:
        notification = request.user.notifications.get(id=notification_id)
        notification.is_read = True
        notification.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Notification marked as read'
        })
    except Notification.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Notification not found'
        }, status=404)

@login_required
@require_POST
def mark_all_notifications_read(request):
    """Mark all notifications as read for the user"""
    count = request.user.notifications.filter(is_read=False).update(is_read=True)
    
    return JsonResponse({
        'success': True,
        'message': f'{count} notifications marked as read',
        'count': count
    })

@login_required
def get_notifications_dropdown(request):
    """Get notifications for dropdown display"""
    notifications = request.user.notifications.all()[:5]  # Last 5 notifications
    unread_count = request.user.notifications.filter(is_read=False).count()
    
    notifications_data = []
    for notification in notifications:
        notifications_data.append({
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'is_read': notification.is_read,
            'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'icon_class': notification.get_icon_class(),
            'timesince': notification.created_at.strftime('%H:%M')
        })
    
    return JsonResponse({
        'notifications': notifications_data,
        'unread_count': unread_count
    })

def create_entrepreneur_notification(user):
    """Create notification for admins when new entrepreneur registers"""
    from .models import Notification
    
    title = "New Entrepreneur Registration"
    message = f"{user.username} has registered as a new entrepreneur on the platform."
    
    Notification.notify_admins(
        notification_type='new_entrepreneur',
        title=title,
        message=message,
        entrepreneur_id=user.id
    )

def create_order_notification(entrepreneur, order):
    """Create notification for entrepreneur when they receive a new order"""
    from .models import Notification
    
    title = "New Order Received"
    message = f"You have received a new order (Order #{order.id}). Total: ${order.total_amount}"
    
    Notification.create_notification(
        recipient=entrepreneur,
        notification_type='new_order',
        title=title,
        message=message,
        order_id=order.id
    )

def create_order_status_notification(customer, order, status):
    """Create notification for customer when order status changes"""
    from .models import Notification
    
    title = f"Order Status Updated"
    message = f"Your order #{order.id} status has been updated to: {status}"
    
    Notification.create_notification(
        recipient=customer,
        notification_type='order_status',
        title=title,
        message=message,
        order_id=order.id
    )
