from django.db import models


class PageMeta(models.Model):
    url = models.CharField(max_length=64, blank=False, null=False, verbose_name="Относительная ссылка на страницу")
    title = models.CharField(max_length=64, blank=False, null=False, verbose_name="Title")
    keywords = models.TextField(max_length=64, blank=True, null=True, verbose_name="Keywords")
    description = models.TextField(max_length=64, blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"Мета данные"
        verbose_name_plural = u"Мета данные"
