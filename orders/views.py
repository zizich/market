from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect

from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


@login_required
def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user  # получаем пользователя
                    cart_items = Cart.objects.filter(user=user)  # выбираем все корзины которые есть у user

                    if cart_items.exists():  # если корзины существуют
                        # Создать заказ
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )
                        # Создать заказанные товары: тут мы работаем с models/OrderItem
                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            price = cart_item.product.sell_price()
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(f'Недостаточное количество товара {name} на складе\
                                                       В наличии - {product.quantity} шт.')

                            # создаем на каждый продукт OrderItem
                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )
                            # обращаемся к количеству
                            product.quantity -= quantity
                            product.save()

                        # Очистить корзину пользователя после создания заказа
                        cart_items.delete()

                        messages.success(request, 'Заказ оформлен!')
                        return redirect('user:profile')
            except ValidationError as e:
                messages.success(request, str(e))
                return redirect('cart:order')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }

        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Home - Оформление заказа',
        'form': form,
        'order': True,
    }
    return render(request, 'orders/create_order.html', context=context)
