from datetime import datetime
from django.db import models
from base.models import ModelWithCategory
from tinymce.models import HTMLField
from utils.make_thumbnail import make_thumbnail
from utils.slugify import slugify


class ProductCategory(ModelWithCategory):
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name="Название")
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Категория продуктов"
        verbose_name_plural = u"Категории продуктов"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductTag(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Параметр продуктов"
        verbose_name_plural = u"Параметры продуктов"


class Characteristic(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Характеристика"
        verbose_name_plural = u"Характеристики"


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, blank=False, null=False, related_name='products',
                                 on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name="Название")
    description = HTMLField(blank=True, verbose_name="Описание")
    price = models.IntegerField(verbose_name="Цена", null=False)
    old_price = models.IntegerField(verbose_name="Старая цена", null=True, blank=True)
    priority = models.IntegerField(verbose_name="Приоритет", default=1)
    slug = models.SlugField(blank=True)
    tags = models.ManyToManyField(ProductTag, related_name='products', blank=True, default=None, verbose_name=u"Параметры")
    hour_rate = models.BooleanField(verbose_name=u"Товар с почасовой оплатой", default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-priority"]
        verbose_name = u"Товар"
        verbose_name_plural = u"Товары"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, blank=False, null=False, related_name='images',
                                on_delete=models.CASCADE, verbose_name="Продукт")
    image = models.ImageField(verbose_name="Изображение", upload_to='static/img/products/')
    thumb = models.ImageField(blank=True, editable=False, upload_to='static/img/products/')
    is_main = models.BooleanField(verbose_name="Главное", default=False)

    def __str__(self):
        return self.product.name

    class Meta:
        ordering = ["-is_main"]
        verbose_name = u"Изображение"
        verbose_name_plural = u"Изображения"

    def save(self, *args, **kwargs):
        if not make_thumbnail(self.image, self.thumb, 422, 468):
            raise Exception('Could not create thumbnail - is the file type valid?')
        super().save(*args, **kwargs)


class ProductCharacteristic(models.Model):
    product = models.ForeignKey(Product, blank=False, null=False, related_name='characteristics',
                                on_delete=models.CASCADE, verbose_name="Продукт")
    characteristic = models.ForeignKey(Characteristic, blank=False, null=False,
                                       on_delete=models.CASCADE, verbose_name="Характеристика")
    value = models.CharField(max_length=64, blank=False, null=False, verbose_name="Значение")

    def __str__(self):
        return self.characteristic.name

    class Meta:
        verbose_name = u"Характеристика продуктов"
        verbose_name_plural = u"Характеристики продуктов"


class ProductUnit(models.Model):
    product = models.ForeignKey(Product, blank=False, null=False, related_name='product_units',
                                on_delete=models.CASCADE, verbose_name="Продукт")
    description = models.TextField(max_length=256, blank=True, verbose_name="Описание")
    article = models.CharField(max_length=128, blank=True, verbose_name="Артикул")

    def __str__(self):
        return self.article

    class Meta:
        verbose_name = u"Единица продуктов"
        verbose_name_plural = u"Единицы продуктов"


class ProductUnitBookingDates(models.Model):
    product_unit = models.ForeignKey(ProductUnit, blank=False, null=False, related_name='booking_dates',
                                on_delete=models.CASCADE, verbose_name="Единица продукта")
    date_from = models.DateTimeField(verbose_name="Бронь от")
    date_to = models.DateTimeField(verbose_name="Бронь до")
    total_price = models.IntegerField(verbose_name="Полная цена", null=True, blank=True)

    def __str__(self):
        return self.product_unit.article

    class Meta:
        verbose_name = u"Бронь"
        verbose_name_plural = u"Брони"

    def save(self, *args, **kwargs):
        price = self.product_unit.product.price
        range = datetime(year=self.date_to.year, month=self.date_to.month, day=self.date_to.day, hour=self.date_to.hour) - \
                datetime(year=self.date_from.year, month=self.date_from.month, day=self.date_from.day, hour=self.date_from.hour)
        if self.product_unit.product.hour_rate:
            self.total_price = (range.seconds // 3600) * price
        else:
            self.total_price = range.days * price
        super().save(*args, **kwargs)
