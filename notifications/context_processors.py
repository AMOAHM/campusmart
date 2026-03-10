from .models import Notification

def notifications_context(request):
    """Add notifications to context for authenticated users"""
    if request.user.is_authenticated and hasattr(request.user, 'notifications'):
        return {
            'notifications': request.user.notifications.all()[:5],
            'unread_notifications': request.user.notifications.filter(is_read=False)
        }
    return {}
