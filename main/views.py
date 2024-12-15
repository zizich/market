from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context = {
        'title': 'Домашняя страница',
        'content': 'Добро пожаловать',
        'list': ['first', 'second'],
        'dict': {'first': 1},
        'bool': True,
    }
    return render(request, 'main/index.html')


def about(request):
    return HttpResponse('О компании')
