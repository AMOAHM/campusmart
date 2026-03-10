from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('<int:pk>/', views.chat_room, name='chat_room'),
    path('support/create/', views.create_support_chat, name='create_support_chat'),
    path('store/<int:store_id>/create/', views.create_store_chat, name='create_store_chat'),
    path('admin/', views.admin_chat_list, name='admin_chat_list'),
]
