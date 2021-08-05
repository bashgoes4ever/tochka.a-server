from django.contrib import admin
from .models import *


class ArticleImagesInline(admin.TabularInline):
    model = ArticleImages
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Article._meta.fields]
    inlines = [ArticleImagesInline]

    class Meta:
        model = Article


admin.site.register(Tag)
admin.site.register(ArticleImages)
admin.site.register(Article, ArticleAdmin)
