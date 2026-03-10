from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db.models import Count, Q, Min, Max, Avg
from django.utils import timezone
from datetime import timedelta
from products.models import Product, Category, Favorite
from stores.models import Store
from orders.models import Order
from notifications.models import Notification
from .models import CarouselImage

User = get_user_model()


def home(request):
    # Get filter parameters
    category_slug = request.GET.get('category', '')
    search_query = request.GET.get('q', '')
    
    # Base queryset
    products = Product.objects.filter(is_active=True)
    
    # Apply filters
    if category_slug:
        products = products.filter(category__name__iexact=category_slug.replace('-', ' '))
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Get featured and latest products
    featured_products = products[:12]
    latest_products = products.order_by('-created_at')[:12]
    
    # Get categories
    categories = Category.objects.all()[:10]
    
    # Get popular stores
    popular_stores = Store.objects.filter(is_active=True)[:6]
    
    # Calculate price statistics
    all_products = Product.objects.filter(is_active=True)
    min_price = all_products.aggregate(Min('price'))['price__min'] or 20
    max_price = all_products.aggregate(Max('price'))['price__max'] or 1130
    avg_price = all_products.aggregate(Avg('price'))['price__avg'] or 300
    
    # Get carousel images
    carousel_images = CarouselImage.objects.filter(is_active=True).order_by('display_order', 'created_at')
    
    # Get user-specific data
    cart_items = []
    user_favorites = []
    if request.user.is_authenticated:
        # Get cart items (you'll need to implement cart model/logic)
        # cart_items = CartItem.objects.filter(user=request.user)
        
        # Get user favorites
        user_favorites = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    
    context = {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'products': featured_products,  # Main products display
        'categories': categories,
        'popular_stores': popular_stores,
        'carousel_images': carousel_images,
        'min_price': min_price,
        'max_price': max_price,
        'avg_price': avg_price,
        'cart_items': cart_items,
        'user_favorites': user_favorites,
        'current_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'home.html', context)


def get_carousel_data(request):
    """API endpoint to get carousel data for frontend"""
    images = CarouselImage.objects.filter(is_active=True).order_by('display_order', 'created_at')
    
    data = []
    for image in images:
        data.append({
            'id': image.id,
            'title': image.title,
            'description': image.description,
            'image_url': image.image_url,
            'is_active': image.is_active,
            'display_order': image.display_order,
        })
    
    return JsonResponse({'images': data})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(is_active=True).filter(
        name__icontains=query
    ) if query else Product.objects.none()
    
    context = {
        'query': query,
        'results': products,
    }
    return render(request, 'search_results.html', context)


def admin_dashboard_view(request):
    """Admin dashboard view with real database statistics"""
    if not request.user.is_staff:
        return redirect('admin:login')
    
    # Get real statistics
    total_users = User.objects.count()
    active_stores = Store.objects.filter(is_active=True).count()
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    
    # Recent activity (last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    
    recent_users = User.objects.filter(date_joined__gte=seven_days_ago).count()
    recent_orders = Order.objects.filter(created_at__gte=seven_days_ago).count()
    recent_stores = Store.objects.filter(created_at__gte=seven_days_ago).count()
    
    # Get recent activity items
    recent_activities = []
    
    # Recent orders
    recent_order_items = Order.objects.order_by('-created_at')[:3]
    for order in recent_order_items:
        recent_activities.append({
            'title': f'New order #{order.id} placed',
            'time': timezone.now() - order.created_at,
            'icon': 'shopping-cart',
            'type': 'primary'
        })
    
    # Recent users
    recent_user_items = User.objects.order_by('-date_joined')[:2]
    for user in recent_user_items:
        recent_activities.append({
            'title': f'New user {user.username} joined',
            'time': timezone.now() - user.date_joined,
            'icon': 'user',
            'type': 'success'
        })
    
    # Recent stores
    recent_store_items = Store.objects.order_by('-created_at')[:2]
    for store in recent_store_items:
        recent_activities.append({
            'title': f'New store "{store.name}" registered',
            'time': timezone.now() - store.created_at,
            'icon': 'store',
            'type': 'warning'
        })
    
    # Sort by time
    recent_activities.sort(key=lambda x: x['time'], reverse=True)
    recent_activities = recent_activities[:5]
    
    # Calculate percentages for quick stats
    total_storage = 100  # This would be calculated based on actual storage usage
    used_storage = 67  # This would be calculated based on actual file sizes
    
    active_users_percentage = min(89, int((recent_users / max(total_users, 1)) * 100))
    server_load = 34  # This would be calculated using system monitoring
    database_usage = 45  # This would be calculated based on actual database size
    
    context = {
        'total_users': total_users,
        'active_stores': active_stores,
        'total_orders': total_orders,
        'total_products': total_products,
        'recent_users': recent_users,
        'recent_orders': recent_orders,
        'recent_stores': recent_stores,
        'recent_activities': recent_activities,
        'used_storage_percentage': used_storage,
        'active_users_percentage': active_users_percentage,
        'server_load_percentage': server_load,
        'database_usage_percentage': database_usage,
    }


def product_detail_redirect(request, pk):
    """Redirect to the actual product detail URL in products app"""
    from django.shortcuts import redirect
    return redirect('products:product_detail', pk=pk)
