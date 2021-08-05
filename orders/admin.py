from django.contrib import admin
from .models import *

class ProductUnitInOrderInline(admin.TabularInline):
    model = ProductUnitInOrder
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    inlines = [ProductUnitInOrderInline]

    class Meta:
        model = Order


admin.site.register(Order, OrderAdmin)
admin.site.register(ProductUnitInOrder)
admin.site.register(FormApplication)