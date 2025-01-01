from django.urls import path  # сопоставляет запросы пользователя с функциями их обработки
from . import views

app_name = "carts"

urlpatterns = [
    path('cart_add/<slug:product_slug>/', views.cart_add, name='cart_add'),
    path('cart_change/<slug:product_slug>/', views.cart_change, name='cart_change'),
    path('cart_remove/<slug:product_slug>/', views.cart_remove, name='cart_remove'),
]
