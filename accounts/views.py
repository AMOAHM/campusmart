from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import User
from django.db.models import Q


@require_http_methods(["GET", "POST"])
def register_customer(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
            return redirect('accounts:register_customer')
        
        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            messages.error(request, 'Username or email already exists')
            return redirect('accounts:register_customer')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            role='customer'
        )
        messages.success(request, 'Account created successfully. Please login.')
        return redirect('accounts:login_customer')
    
    return render(request, 'accounts/register_customer.html')


@require_http_methods(["GET", "POST"])
def register_entrepreneur(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
            return redirect('accounts:register_entrepreneur')
        
        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            messages.error(request, 'Username or email already exists')
            return redirect('accounts:register_entrepreneur')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            role='entrepreneur'
        )
        messages.success(request, 'Account created. Awaiting admin approval to assign store.')
        return redirect('accounts:login_entrepreneur')
    
    return render(request, 'accounts/register_entrepreneur.html')


@require_http_methods(["GET", "POST"])
def login_customer(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role == 'customer':
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials or not a customer account')
            return redirect('accounts:login_customer')
    
    return render(request, 'accounts/login_customer.html')


@require_http_methods(["GET", "POST"])
def login_entrepreneur(request):
    if request.user.is_authenticated:
        return redirect('stores:entrepreneur_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role == 'entrepreneur':
            if hasattr(user, 'store') and user.store:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('stores:entrepreneur_dashboard')
            else:
                messages.error(request, 'No store assigned yet. Please contact admin.')
                return redirect('accounts:login_entrepreneur')
        else:
            messages.error(request, 'Invalid credentials or not an entrepreneur account')
            return redirect('accounts:login_entrepreneur')
    
    return render(request, 'accounts/login_entrepreneur.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request):
    context = {'user': request.user}
    return render(request, 'accounts/profile.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def profile_edit(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.phone_number = phone_number
        request.user.save()
        
        messages.success(request, 'Profile updated successfully.')
        return redirect('accounts:profile')
    
    context = {'user': request.user}
    return render(request, 'accounts/profile_edit.html', context)

