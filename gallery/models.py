from django.db import models
from utils.make_thumbnail import make_thumbnail
from utils.slugify import slugify


class GalleryCategory(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name="Название")
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Категория"
        verbose_name_plural = u"Категории"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class GalleryImage(models.Model):
    category = models.ForeignKey(GalleryCategory, blank=False, null=False, related_name='images',
                                on_delete=models.CASCADE, verbose_name="Категория")
    image = models.ImageField(verbose_name="Изображение", upload_to='static/img/gallery/')
    thumb = models.ImageField(blank=True, editable=False, upload_to='static/img/gallery/')
    priority = models.IntegerField(verbose_name="Приоритет", default=1)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-priority"]
        verbose_name = u"Изображение"
        verbose_name_plural = u"Изображения"

    def save(self, *args, **kwargs):
        if not make_thumbnail(self.image, self.thumb, 375, 246):
            raise Exception('Could not create thumbnail - is the file type valid?')
        super().save(*args, **kwargs)


class Review(models.Model):
    image = models.ImageField(verbose_name="Изображение", upload_to='static/img/reviews/')
    thumb = models.ImageField(blank=True, editable=False, upload_to='static/img/reviews/')
    priority = models.IntegerField(verbose_name="Приоритет", default=1)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-priority"]
        verbose_name = u"Отзыв"
        verbose_name_plural = u"Отзывы"

    def save(self, *args, **kwargs):
        if not make_thumbnail(self.image, self.thumb, 210, 414):
            raise Exception('Could not create thumbnail - is the file type valid?')
        super().save(*args, **kwargs)