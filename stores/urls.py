from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('', views.stores_list, name='stores_list'),
    path('<int:pk>/', views.store_detail, name='store_detail'),
    path('dashboard/', views.entrepreneur_dashboard, name='entrepreneur_dashboard'),
]
