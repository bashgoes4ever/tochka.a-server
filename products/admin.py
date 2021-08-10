from django.contrib import admin
from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductCharacteristicInline(admin.TabularInline):
    model = ProductCharacteristic
    extra = 1


class ProductUnitInline(admin.TabularInline):
    model = ProductUnit
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price')
    inlines = [ProductImageInline, ProductCharacteristicInline, ProductUnitInline]
    search_fields = ('name',)

    class Meta:
        model = Product


class ProductUnitBookingDatesInline(admin.TabularInline):
    model = ProductUnitBookingDates
    extra = 1


class ProductUnitAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductUnit._meta.fields]
    inlines = [ProductUnitBookingDatesInline]

    class Meta:
        model = ProductUnit


admin.site.register(ProductCategory)
admin.site.register(ProductTag)
admin.site.register(Characteristic)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductUnit, ProductUnitAdmin)
admin.site.register(ProductUnitBookingDates)

