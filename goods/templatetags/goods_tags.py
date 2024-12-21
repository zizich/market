from django.utils.http import urlencode

from goods.models import Categories
from django import template

register = template.Library()


@register.simple_tag()
def categories_tags():
    return Categories.objects.all()


@register.simple_tag(takes_context=True)  # все контекстные переменные попадут в функцию, которые передаются с views
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
