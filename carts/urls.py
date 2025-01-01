from django.urls import path  # сопоставляет запросы пользователя с функциями их обработки
from . import views

app_name = "carts"

urlpatterns = [
    path('cart_add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart_change/<int:product_id>/', views.cart_change, name='cart_change'),
    path('cart_remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]
