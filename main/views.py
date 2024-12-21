from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories


def index(request):

    context = {
        'title': 'Home - Главная страница',
        'content': 'Магазин мебели HOME',
    }
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'Home - О компании',
        'content': 'О компании',
        'text_on_page': 'Текст о том почему этот магазин такой классный',
    }
    return render(request, 'main/about.html', context)
