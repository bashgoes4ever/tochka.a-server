from django.contrib import admin
from .models import *


class TourStepInline(admin.TabularInline):
    model = TourStep
    extra = 1


class TourHowToFindImagesInline(admin.TabularInline):
    model = TourHowToFindImages
    extra = 1


class TourInterestingPlacesImagesInline(admin.TabularInline):
    model = TourInterestingPlacesImages
    extra = 1


class TourInventoryImagesInline(admin.TabularInline):
    model = TourInventoryImages
    extra = 1


class TourAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Tour._meta.fields]
    inlines = [TourStepInline, TourHowToFindImagesInline, TourInterestingPlacesImagesInline, TourInventoryImagesInline]

    class Meta:
        model = Tour


admin.site.register(Tour, TourAdmin)
admin.site.register(Guide)
admin.site.register(FAQItem)
admin.site.register(TourStep)
admin.site.register(TourHowToFindImages)
admin.site.register(TourInterestingPlacesImages)
admin.site.register(TourInventoryImages)
