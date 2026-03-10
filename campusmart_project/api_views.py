from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from products.models import Product, Favorite
from orders.models import Cart, CartItem
import json

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def add_to_favorites(request, product_id):
    """Add product to user favorites"""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
        
        if created:
            return JsonResponse({'success': True, 'message': 'Added to favorites'})
        else:
            return JsonResponse({'success': True, 'message': 'Already in favorites'})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def add_to_cart_api(request, product_id):
    """Add product to user cart"""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        
        # Get or create cart for user
        cart, created = Cart.objects.get_or_create(customer=request.user)
        
        # Check if item already in cart
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
        
        if not item_created:
            # Increment quantity if already exists
            cart_item.quantity += 1
            cart_item.save()
        
        # Calculate cart total
        cart_items = CartItem.objects.filter(cart=cart)
        total_items = sum(item.quantity for item in cart_items)
        
        return JsonResponse({
            'success': True, 
            'message': 'Added to cart successfully',
            'cart_count': total_items
        })
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def remove_from_favorites(request, product_id):
    """Remove product from user favorites"""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        deleted_count, _ = Favorite.objects.filter(user=request.user, product=product).delete()
        
        if deleted_count > 0:
            return JsonResponse({'success': True, 'message': 'Removed from favorites'})
        else:
            return JsonResponse({'success': True, 'message': 'Not in favorites'})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
