from django.urls import path  # сопоставляет запросы пользователя с функциями их обработки
from . import views

app_name = "orders"

urlpatterns = [
    path('create-order/', views.CreateOrderView.as_view(), name='create_order'),
    ]
