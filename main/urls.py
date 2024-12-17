from django.urls import path  # сопоставляет запросы пользователя с функциями их обработки
from . import views

app_name = "main"

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]
