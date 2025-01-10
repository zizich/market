from django.contrib import admin
from .models import Categories, Products

# admin.site.register(Categories)
# admin.site.register(Products)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


# Административная часть где можно менять поля, управлять ими
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # показать в админке все продукты по именам
    list_display = ['name', 'quantity', 'price', 'discount']  # показать перечисленные поля
    list_editable = ['discount',]  # поля для того, чтобы изменить продукт в админке
    search_fields = ['name', 'description']  # добавить в админке поле для поиска по перечисленным параметрам
    list_filter = ['discount', 'quantity', 'category']  # сортировать товары по след. параметрам
    fields = [
        'name', 'category', 'slug', 'description', 'image', ('price', 'discount'), 'quantity'
    ]  # поле для самого продукта
