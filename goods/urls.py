from django.urls import path  # сопоставляет запросы пользователя с функциями их обработки
from . import views

app_name = "goods"

urlpatterns = [
    path('', views.catalog, name='index'),
    path('product/<slug:product_slug>/', views.product, name='product'),
]
