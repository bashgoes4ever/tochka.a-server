from django.db import models
from products.models import Product


class Basket(models.Model):
    user = models.CharField(max_length=64, blank=False, null=False)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = u"Корзина"
        verbose_name_plural = u"Корзины"


class ProductInBasket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False, verbose_name="Товар")
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, blank=False, null=False, verbose_name="Корзина", related_name="products")
    quantity = models.IntegerField(verbose_name="Количество")

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = u"Товар в корзине"
        verbose_name_plural = u"Товары в корзине"

