from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('title', 'product_type', 'price')


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('title', )


@admin.register(Customer)
class CustomerAdmin(TranslationAdmin):
    list_display = ('user',)


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('customer','product', 'quantity')
    list_filter = ('customer', 'product')


class ShippingInline(admin.TabularInline):
    model = Shipping
    extra = 1


# @admin.register(Shipping)
# class ShippingAdmin(admin.ModelAdmin):
#     list_display = ('customer','date_shipping')
#     list_filter = ('customer','date_shipping')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ShippingInline,]

admin.site.register(Basket)
# admin.site.register(Order)
admin.site.register(Image)

