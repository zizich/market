from django.urls import path  # сопоставляет запросы пользователя с функциями их обработки
from . import views

app_name = "orders"

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
    ]
