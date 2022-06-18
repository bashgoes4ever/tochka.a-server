from django.contrib import admin
from .models import *

class ProductUnitInOrderInline(admin.TabularInline):
    model = ProductUnitInOrder
    exclude = ('quantity',)
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    list_display.remove('basket')
    inlines = [ProductUnitInOrderInline]

    class Meta:
        model = Order


admin.site.register(Order, OrderAdmin)
admin.site.register(ProductUnitInOrder)
admin.site.register(FormApplication)