from django.db import models

from goods.models import Products
from users.models import User


class CartQuerySet(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    # в переменную user добавили blank=True, null=True для возможности добавление товара в корзину
    # даже если пользователь не зарегистрирован
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    # Ключ сессии, она добавляется в БД не по пользователю, а по ключу сессии. Если не авторизованный
    # пользователь добавил товар
    session_key = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'cart'
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

    objects = CartQuerySet.as_manager()

    def products_price(self):
        return round(self.product.sale_price() * self.quantity, 2)

    def __str__(self):
        return f"Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}"
