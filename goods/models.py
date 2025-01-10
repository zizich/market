from django.db import models
from django.urls import reverse


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    objects = models.Manager()

    class Meta:
        db_table = 'category'
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(upload_to="goods_image", blank=True, null=True, verbose_name="Изображение")
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name="Цена")
    discount = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name="Скидка в %")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    category = models.ForeignKey(to="Categories", on_delete=models.SET_DEFAULT,
                                 default="Другие категории", verbose_name="Категория")

    objects = models.Manager()

    class Meta:
        db_table = 'product'
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

        ordering = ('id',)

    def __str__(self):
        return f"{self.name} Количество - {self.quantity}"

    # при применении этого метода можно не пользоваться тегом url, и где ссылка href можно
    # пользоваться Product.get_absolute_url. Также в админке появится кнопка посмотреть на сайте
    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'product_slug': self.slug})

    def display_id(self):
        return f'{self.id:05}'

    def sale_price(self):
        if self.discount:
            return round(float(self.price) - ((float(self.price) * float(self.discount)) / 100), 2)
        return self.price
