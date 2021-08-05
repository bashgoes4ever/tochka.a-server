from django.db import models
from utils.make_thumbnail import make_thumbnail
from tinymce.models import HTMLField


class Tag(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Рубрика"
        verbose_name_plural = u"Рубрики"


class Article(models.Model):
    tags = models.ManyToManyField(Tag, blank=True, default=None, verbose_name=u"Рубрики")
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name="Заголовок")
    image = models.ImageField(verbose_name="Фото", upload_to='static/img/blog/')
    thumb = models.ImageField(blank=True, editable=False, upload_to='static/img/blog/')
    description = HTMLField(blank=True, verbose_name="Короткое описание")
    content1 = HTMLField(blank=True, verbose_name="Контент до слайдера")
    content2 = HTMLField(blank=True, verbose_name="Контент после слайдера")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Пост"
        verbose_name_plural = u"Посты"

    def save(self, *args, **kwargs):
        if not make_thumbnail(self.image, self.thumb, 764, 440):
            raise Exception('Could not create thumbnail - is the file type valid?')
        super().save(*args, **kwargs)


class ArticleImages(models.Model):
    article = models.ForeignKey(Article, blank=False, null=False, related_name='images',
                                 on_delete=models.CASCADE, verbose_name="Тур")
    image = models.ImageField(verbose_name="Изображение", upload_to='static/img/blog/')
    thumb = models.ImageField(blank=True, editable=False, upload_to='static/img/blog/')
    priority = models.IntegerField(verbose_name="Приоритет", default=1)

    def __str__(self):
        return self.article.name

    class Meta:
        ordering = ["-priority"]
        verbose_name = u"Изображение (слайдер)"
        verbose_name_plural = u"Изображения (слайдер)"

    def save(self, *args, **kwargs):
        if not make_thumbnail(self.image, self.thumb, 374, 256):
            raise Exception('Could not create thumbnail - is the file type valid?')
        super().save(*args, **kwargs)
