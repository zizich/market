from carts.models import Cart


# получаем всю корзину пользователя
def get_user_carts(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)
