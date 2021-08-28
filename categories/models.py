from django.db import models
from tinymce.models import HTMLField
from products.models import ProductCategory
from base.models import ModelWithCategory
from utils.make_thumbnail import make_thumbnail


class CategoryCard(ModelWithCategory):
    title = HTMLField(blank=True, verbose_name="Заголовок")
    categories = models.ManyToManyField(ProductCategory, blank=True, default=None,
                                        verbose_name=u"Дочерние категорие, которые будут показаны")
    description = HTMLField(blank=True, verbose_name="Описание")
    image = models.ImageField(verbose_name="Изображение", blank=True, upload_to='static/img/categories/')
    thumb = models.ImageField(blank=True, editable=False, upload_to='static/img/categories/')
    show_link = models.BooleanField(verbose_name="Показывать кнопку 'подробнее'", default=True)
    custom_link = models.CharField(blank=True, max_length=64, verbose_name="Своя ссылка")
    priority = models.IntegerField(verbose_name="Приоритет", default=1)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-priority"]
        verbose_name = u"Категория на главной"
        verbose_name_plural = u"Категории на главной"

    def save(self, *args, **kwargs):
        if not make_thumbnail(self.image, self.thumb, 568, 250):
            raise Exception('Could not create thumbnail - is the file type valid?')
        super().save(*args, **kwargs)

