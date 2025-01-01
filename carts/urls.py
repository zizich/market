from django.urls import path  # сопоставляет запросы пользователя с функциями их обработки
from . import views

app_name = "carts"

urlpatterns = [
    path('search/', views.catalog, name='search'),
    path('<slug:category_slug>/', views.catalog, name='index'),
    path('product/<slug:product_slug>/', views.product, name='product'),
]