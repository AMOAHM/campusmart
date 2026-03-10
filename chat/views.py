from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import JsonResponse
from .models import ChatRoom, ChatMessage
from stores.models import Store


@login_required
@require_http_methods(["GET"])
def chat_list(request):
    if request.user.role != 'customer':
        messages.error(request, 'Only customers can access chat.')
        return redirect('home')
    
    chat_rooms = request.user.chat_rooms.all()
    context = {'chat_rooms': chat_rooms}
    return render(request, 'chat/chat_list.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def chat_room(request, pk):
    chat_room_obj = get_object_or_404(ChatRoom, pk=pk)
    
    if request.user.role == 'customer' and chat_room_obj.customer != request.user:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        message_text = request.POST.get('message')
        
        if message_text:
            ChatMessage.objects.create(
                chat_room=chat_room_obj,
                sender=request.user,
                message=message_text,
            )
            messages.success(request, 'Message sent.')
        
        return redirect('chat:chat_room', pk=pk)
    
    chat_messages = chat_room_obj.messages.all()
    context = {
        'chat_room': chat_room_obj,
        'messages': chat_messages,
    }
    return render(request, 'chat/chat_room.html', context)


@login_required
@require_http_methods(["GET"])
def create_support_chat(request):
    if request.user.role != 'customer':
        messages.error(request, 'Only customers can create support chat.')
        return redirect('home')
    
    # Check if customer already has a support chat
    existing_chat = ChatRoom.objects.filter(
        customer=request.user,
        room_type='support'
    ).first()
    
    if existing_chat:
        return redirect('chat:chat_room', pk=existing_chat.pk)
    
    # Create new support chat
    chat_room_obj = ChatRoom.objects.create(
        customer=request.user,
        room_type='support',
    )
    
    messages.success(request, 'Support chat created.')
    return redirect('chat:chat_room', pk=chat_room_obj.pk)


@login_required
@require_http_methods(["GET", "POST"])
def create_store_chat(request, store_id):
    if request.user.role != 'customer':
        messages.error(request, 'Only customers can create store chat.')
        return redirect('home')
    
    store = get_object_or_404(Store, pk=store_id)
    
    # Check if customer already has a chat with this store
    existing_chat = ChatRoom.objects.filter(
        customer=request.user,
        store=store,
        room_type='entrepreneur'
    ).first()
    
    if existing_chat:
        return redirect('chat:chat_room', pk=existing_chat.pk)
    
    if request.method == 'POST':
        # Create new chat
        chat_room_obj = ChatRoom.objects.create(
            customer=request.user,
            store=store,
            room_type='entrepreneur',
        )
        
        messages.success(request, f'Chat with {store.name} created.')
        return redirect('chat:chat_room', pk=chat_room_obj.pk)
    
    context = {'store': store}
    return render(request, 'chat/create_store_chat.html', context)


@login_required
@require_http_methods(["GET"])
def admin_chat_list(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    chat_rooms = ChatRoom.objects.filter(room_type='support')
    context = {'chat_rooms': chat_rooms}
    return render(request, 'admin/chat_list.html', context)

