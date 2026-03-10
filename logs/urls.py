from django.urls import path
from . import views

app_name = 'logs'

urlpatterns = [
    path('', views.logs_view, name='logs_view'),
]

