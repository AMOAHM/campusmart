from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from stores.models import Store
import uuid


@login_required
@require_http_methods(["GET"])
def cart_view(request):
    if request.user.role != 'customer':
        messages.error(request, 'Only customers can view cart.')
        return redirect('home')
    
    cart, created = Cart.objects.get_or_create(customer=request.user)
    context = {'cart': cart}
    return render(request, 'orders/cart.html', context)


@login_required
@require_http_methods(["POST"])
def add_to_cart(request, product_id):
    if request.user.role != 'customer':
        messages.error(request, 'Only customers can add to cart.')
        return redirect('home')
    
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart, created = Cart.objects.get_or_create(customer=request.user)
    
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart.')
    return redirect('products:product_detail', pk=product_id)


@login_required
@require_http_methods(["POST"])
def remove_from_cart(request, item_id):
    if request.user.role != 'customer':
        messages.error(request, 'Only customers can remove from cart.')
        return redirect('home')
    
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__customer=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('orders:cart_view')


@login_required
@require_http_methods(["GET", "POST"])
def checkout(request):
    if request.user.role != 'customer':
        messages.error(request, 'Only customers can checkout.')
        return redirect('home')
    
    cart, created = Cart.objects.get_or_create(customer=request.user)
    
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('orders:cart_view')
    
    if request.method == 'POST':
        delivery_name = request.POST.get('delivery_name')
        delivery_phone = request.POST.get('delivery_phone')
        delivery_location = request.POST.get('delivery_location')
        delivery_notes = request.POST.get('delivery_notes', '')
        
        if not all([delivery_name, delivery_phone, delivery_location]):
            messages.error(request, 'All required fields must be filled.')
            return redirect('orders:checkout')
        
        # Group cart items by store
        cart_items = cart.items.all()
        stores = set(item.product.store for item in cart_items)
        
        orders_created = []
        
        for store in stores:
            store_items = [item for item in cart_items if item.product.store == store]
            total_price = sum(item.get_total_price() for item in store_items)
            
            order_id = f"ORD{uuid.uuid4().hex[:8].upper()}"
            
            order = Order.objects.create(
                order_id=order_id,
                customer=request.user,
                store=store,
                total_price=total_price,
                delivery_name=delivery_name,
                delivery_phone=delivery_phone,
                delivery_location=delivery_location,
                delivery_notes=delivery_notes,
            )
            
            for item in store_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
            
            orders_created.append(order)
        
        # Clear cart
        cart.items.all().delete()
        
        messages.success(request, f'{len(orders_created)} order(s) placed successfully!')
        return redirect('orders:order_history')
    
    # Calculate number of unique stores in cart
    cart_items = cart.items.all()
    unique_stores = len(set(item.product.store for item in cart_items)) if cart_items.exists() else 1
    
    context = {'cart': cart, 'unique_stores_count': unique_stores}
    return render(request, 'orders/checkout.html', context)


@login_required
@require_http_methods(["GET"])
def order_history(request):
    if request.user.role == 'customer':
        orders = request.user.orders.all()
    elif request.user.role == 'entrepreneur':
        if not hasattr(request.user, 'store'):
            messages.error(request, 'No store assigned.')
            return redirect('home')
        orders = request.user.store.orders.all()
    else:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    context = {'orders': orders}
    return render(request, 'orders/order_history.html', context)


@login_required
@require_http_methods(["GET"])
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    # Check if user has permission to view order
    if request.user.role == 'customer' and order.customer != request.user:
        messages.error(request, 'Access denied.')
        return redirect('home')
    elif request.user.role == 'entrepreneur' and order.store != request.user.store:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    context = {'order': order}
    return render(request, 'orders/order_detail.html', context)


@login_required
@require_http_methods(["POST"])
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.user.role != 'entrepreneur' or order.store != request.user.store:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    new_status = request.POST.get('status')
    if new_status in ['pending', 'approved', 'out_for_delivery', 'delivered', 'cancelled']:
        order.status = new_status
        
        if new_status == 'delivered':
            order.delivered_at = timezone.now()
        
        order.save()
        messages.success(request, 'Order status updated.')
    else:
        messages.error(request, 'Invalid status.')
    
    return redirect('orders:order_detail', pk=pk)

