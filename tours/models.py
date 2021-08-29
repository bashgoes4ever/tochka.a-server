from django.db import models
from utils.slugify import slugify
from utils.make_thumbnail import make_thumbnail
from tinymce.models import HTMLField


class Guide(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name="Имя")
    description = HTMLField(blank=True, verbose_name="Описание")
    image = models.ImageField(verbose_name="Фото", upload_to='static/img/tours/')
    thumb = models.ImageField(blank=True, editable=False, upload_to='static/img/tours/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Гид"
        verbose_name_plural = u"Гиды"

    def save(self, *args, **kwargs):
        if not make_thumbnail(self.image, self.thumb, 197, 271):
            raise Exception('Could not create thumbnail - is the file type valid?')
        super().save(*args, **kwargs)


class FAQItem(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name="Вопрос")
    description = HTMLField(blank=True, verbose_name="Ответ")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Вопрос"
        verbose_name_plural = u"Вопросы"


class Tour(models.Model):
    short_name = models.CharField(max_length=64, blank=False, null=False, verbose_name="Короткое название")
    short_description = HTMLField(blank=True, verbose_name="Короткое описание")
    card_image = models.ImageField(verbose_name="Изображение в карточке", upload_to='static/img/tours/')
    card_thumb = models.ImageField(blank=True, editable=False, upload_to='static/img/tours/')
    detail_name = HTMLField(blank=True, verbose_name="Название на детальной странице")
    detail_image = models.ImageField(verbose_name="Изображение на детальной странице", upload_to='static/img/tours/')
    detail_thumb = models.ImageField(blank=True, editable=False, upload_to='static/img/tours/')
    groups_from = models.IntegerField(verbose_name="Размер группы от", null=False)
    groups_to = models.IntegerField(verbose_name="Размер группы до", null=True, blank=True)
    duration = models.CharField(max_length=64, blank=False, null=False, verbose_name="Время в туре")
    price = models.IntegerField(verbose_name="Цена", null=False)
    how_to_find = HTMLField(blank=True, verbose_name="Как добраться")
    interesting_places = HTMLField(blank=True, verbose_name="Интересные места")
    video_url = models.TextField(blank=True, verbose_name="Встроенное видео")
    video_image = models.ImageField(verbose_name="Превью видео", blank=True, upload_to='static/img/tours/')
    video_thumb = models.ImageField(blank=True, editable=False, upload_to='static/img/tours/')
    inventory_text = HTMLField(blank=True, verbose_name="Что будем брать с собой")
    guides = models.ManyToManyField(Guide, blank=True, default=None, verbose_name=u"Гиды")
    faq_items = models.ManyToManyField(FAQItem, blank=True, default=None, verbose_name=u"Вопросы")
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = u"Тур"
        verbose_name_plural = u"Туры"

    def save(self, *args, **kwargs):
        if not make_thumbnail(self.card_image, self.card_thumb, 371, 239):
            raise Exception('Could not create thumbnail - is the file type valid?')
        if not make_thumbnail(self.detail_image, self.detail_thumb, 1920, 861):
            raise Exception('Could not create thumbnail - is the file type valid?')
        if self.video_image and not make_thumbnail(self.video_image, self.video_thumb, 962, 440):
            raise Exception('Could not create thumbnail - is the file type valid?')
        self.slug = slugify(self.short_name)
        super().save(*args, **kwargs)


class TourStep(models.Model):
    tour = models.ForeignKey(Tour, blank=False, null=False, related_name='steps',
                                 on_delete=models.CASCADE, verbose_name="Тур")
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name="Название")
    description = HTMLField(blank=True, verbose_name="Описание")
    image = models.ImageField(verbose_name="Изображение", upload_to='static/img/tours/')
    thumb = models.ImageField(blank=True, editable=False, upload_to='static/img/tours/')
    priority = models.IntegerField(verbose_name="Порядковый номер", default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['priority']
        verbose_name = u"Этап тура"
        verbose_name_plural = u"Этапы тура"

    def save(self, *args, **kwargs):
        if not make_thumbnail(self.image, self.thumb, 371, 239):
            raise Exception('Could not create thumbnail - is the file type valid?')
        super().save(*args, **kwargs)


class TourHowToFindImages(models.Model):
    tour = models.ForeignKey(Tour, blank=False, null=False, related_name='htfimgs',
                                 on_delete=models.CASCADE, verbose_name="Тур")
    image = models.ImageField(verbose_name="Изображение", upload_to='static/img/tours/')
    thumb = models.ImageField(blank=True, editable=False, upload_to='static/img/tours/')
    priority = models.IntegerField(verbose_name="Приоритет", default=1)

    def __str__(self):
        return self.tour.short_name

    class Meta:
        ordering = ['-priority']
        verbose_name = u"Изображение (как добраться)"
        verbose_name_plural = u"Изображения (как добраться)"

    def save(self, *args, **kwargs):
        if not make_thumbnail(self.image, self.thumb, 472, 256):
            raise Exception('Could not create thumbnail - is the file type valid?')
        super().save(*args, **kwargs)


class TourInterestingPlacesImages(models.Model):
    tour = models.ForeignKey(Tour, blank=False, null=False, related_name='itimgs',
                                 on_delete=models.CASCADE, verbose_name="Тур")
    image = models.ImageField(verbose_name="Изображение", upload_to='static/img/tours/')
    thumb = models.ImageField(blank=True, editable=False, upload_to='static/img/tours/')
    priority = models.IntegerField(verbose_name="Приоритет", default=1)

    def __str__(self):
        return self.tour.short_name

    class Meta:
        ordering = ['-priority']
        verbose_name = u"Изображение (интересные места)"
        verbose_name_plural = u"Изображения (интересные места)"

    def save(self, *args, **kwargs):
        if not make_thumbnail(self.image, self.thumb, 472, 256):
            raise Exception('Could not create thumbnail - is the file type valid?')
        super().save(*args, **kwargs)


class TourInventoryImages(models.Model):
    tour = models.ForeignKey(Tour, blank=False, null=False, related_name='inventory_imgs',
                                 on_delete=models.CASCADE, verbose_name="Тур")
    image = models.ImageField(verbose_name="Изображение", upload_to='static/img/tours/')
    thumb = models.ImageField(blank=True, editable=False, upload_to='static/img/tours/')
    priority = models.IntegerField(verbose_name="Приоритет", default=1)

    def __str__(self):
        return self.tour.short_name

    class Meta:
        ordering = ['-priority']
        verbose_name = u"Изображение (Что будем брать с собой)"
        verbose_name_plural = u"Изображения (Что будем брать с собой)"

    def save(self, *args, **kwargs):
        if not make_thumbnail(self.image, self.thumb, 305, 256):
            raise Exception('Could not create thumbnail - is the file type valid?')
        super().save(*args, **kwargs)
