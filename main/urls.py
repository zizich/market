from django.urls import path  # сопоставляет запросы пользователя с функциями их обработки
from django.views.decorators.cache import cache_page

from .views import IndexView, AboutView

app_name = "main"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', cache_page(60)(AboutView.as_view()), name='about'),
]
