from goods.models import Categories
from django import template

register = template.Library()


@register.simple_tag()
def categories_tags():
    return Categories.objects.all()
