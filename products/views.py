from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Product, Category, Review
from django.db.models import Q


@require_http_methods(["GET"])
def products_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    product_type = request.GET.get('type', '')
    
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if product_type:
        products = products.filter(product_type=product_type)
    
    # Sort by latest or featured
    sort_by = request.GET.get('sort', '-created_at')
    products = products.order_by(sort_by)
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_type': product_type,
    }
    return render(request, 'products/products_list.html', context)


@require_http_methods(["GET"])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    reviews = product.product_reviews.all()
    similar_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(pk=pk)[:5]
    
    context = {
        'product': product,
        'reviews': reviews,
        'similar_products': similar_products,
    }
    return render(request, 'products/product_detail.html', context)


@require_http_methods(["GET"])
def categories_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'products/categories_list.html', context)


@require_http_methods(["GET"])
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = category.products.filter(is_active=True)
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'products/category_detail.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def add_product(request):
    if request.user.role != 'entrepreneur' or not hasattr(request.user, 'store'):
        messages.error(request, 'You do not have access to this page.')
        return redirect('home')
    
    store = request.user.store
    categories = Category.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity', 0)
        product_type = request.POST.get('product_type', 'product')
        image = request.FILES.get('image')
        
        if not all([name, category_id, description, price, image]):
            messages.error(request, 'All fields are required.')
            return redirect('products:add_product')
        
        category = get_object_or_404(Category, pk=category_id)
        
        product = Product.objects.create(
            store=store,
            name=name,
            category=category,
            description=description,
            price=price,
            quantity=quantity,
            product_type=product_type,
            image=image,
        )
        
        messages.success(request, 'Product added successfully.')
        return redirect('stores:entrepreneur_dashboard')
    
    context = {
        'categories': categories,
        'store': store,
    }
    return render(request, 'entrepreneur/add_product.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def edit_product(request, pk):
    if request.user.role != 'entrepreneur':
        messages.error(request, 'You do not have access to this page.')
        return redirect('home')
    
    product = get_object_or_404(Product, pk=pk, store=request.user.store)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.category_id = request.POST.get('category')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity', 0)
        product.product_type = request.POST.get('product_type', 'product')
        
        if 'image' in request.FILES:
            product.image = request.FILES.get('image')
        
        product.save()
        messages.success(request, 'Product updated successfully.')
        return redirect('stores:entrepreneur_dashboard')
    
    context = {
        'product': product,
        'categories': categories,
    }
    return render(request, 'entrepreneur/edit_product.html', context)


@login_required
@require_http_methods(["POST"])
def delete_product(request, pk):
    if request.user.role != 'entrepreneur':
        messages.error(request, 'You do not have access to this action.')
        return redirect('home')
    
    product = get_object_or_404(Product, pk=pk, store=request.user.store)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('stores:entrepreneur_dashboard')


@login_required
@require_http_methods(["GET", "POST"])
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    
    if request.user.role != 'customer':
        messages.error(request, 'Only customers can leave reviews.')
        return redirect('products:product_detail', pk=pk)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text', '')
        
        review, created = Review.objects.get_or_create(
            product=product,
            customer=request.user,
            defaults={'rating': rating, 'review_text': review_text}
        )
        
        if not created:
            review.rating = rating
            review.review_text = review_text
            review.save()
        
        messages.success(request, 'Review submitted successfully.')
        return redirect('products:product_detail', pk=pk)
    
    return redirect('products:product_detail', pk=pk)

