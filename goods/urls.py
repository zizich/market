from django.urls import path  # сопоставляет запросы пользователя с функциями их обработки
from . import views

app_name = "goods"

urlpatterns = [
    path('search/', views.CatalogView.as_view(), name='search'),
    path('<slug:category_slug>/', views.CatalogView.as_view(), name='index'),
    path('product/<slug:product_slug>/', views.ProductView.as_view(), name='product'),
]
