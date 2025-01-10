from django.contrib import admin

from carts.models import Cart


# admin.site.register(Cart)

# Отображение товаров у каждого пользователя в самом пользователе, внизу
class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = ['product', 'quantity', 'created_timestamp', ]  # показывает товар, количество и дата добавления
    search_fields = ['product', 'quantity', 'created_timestamp', ]  # поиск показывает товар, количество и дата добав.
    readonly_fields = ('created_timestamp',)
    extra = 1  # функция по добавлению товара по одному (1)


# Отображение в корзине товаров у каждого пользователя
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user_display', 'product_display', 'quantity', 'created_timestamp', ]
    list_filter = ['created_timestamp', 'user', 'product__name', ]

    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Анонимный пользователь"

    def product_display(self, obj):
        return str(obj.product.name)
