from django.urls import path  # сопоставляет запросы пользователя с функциями их обработки
from . import views

app_name = "carts"

urlpatterns = [
    path('cart_add/', views.CartAddView.as_view(), name='cart_add'),
    path('cart_change/', views.CartChangeView.as_view(), name='cart_change'),
    path('cart_remove/', views.CartRemoveView.as_view(), name='cart_remove'),
]
