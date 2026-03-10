from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Store
from products.models import Product


@require_http_methods(["GET"])
def stores_list(request):
    stores = Store.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        stores = stores.filter(name__icontains=search_query)
    
    context = {
        'stores': stores,
        'search_query': search_query,
    }
    return render(request, 'stores/stores_list.html', context)


@require_http_methods(["GET"])
def store_detail(request, pk):
    store = get_object_or_404(Store, pk=pk, is_active=True)
    products = store.products.filter(is_active=True)
    
    context = {
        'store': store,
        'products': products,
    }
    return render(request, 'stores/store_detail.html', context)


@login_required
@require_http_methods(["GET"])
def entrepreneur_dashboard(request):
    if request.user.role != 'entrepreneur':
        messages.error(request, 'You do not have access to this page.')
        return redirect('home')
    
    if not hasattr(request.user, 'store'):
        context = {'message': 'No store assigned yet. Please contact admin.'}
        return render(request, 'errors/no_store.html', context)
    
    store = request.user.store
    products = store.products.all()
    orders = store.orders.all()
    
    context = {
        'store': store,
        'products': products,
        'orders': orders,
        'total_products': products.count(),
        'total_orders': orders.count(),
        'pending_orders': orders.filter(status='pending').count(),
    }
    return render(request, 'entrepreneur/dashboard.html', context)

