from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/entrepreneur/', views.register_entrepreneur, name='register_entrepreneur'),
    path('login/customer/', views.login_customer, name='login_customer'),
    path('login/entrepreneur/', views.login_entrepreneur, name='login_entrepreneur'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
