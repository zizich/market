from django.urls import path  # сопоставляет запросы пользователя с функциями их обработки
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]
