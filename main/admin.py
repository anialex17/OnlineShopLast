from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin
from django.contrib.contenttypes.admin import GenericTabularInline


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_type', 'price')
    prepopulated_fields = {'url': ('title',)}
    save_on_top = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )
    prepopulated_fields = {'url': ('title',)}


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('customer','product', 'quantity')
    list_filter = ('customer', 'product')


class ProductItemInline(admin.TabularInline):
    model = ProductItem
    extra=1
#
# class ShippingInline(admin.TabularInline):
#     model = Shipping
#     extra = 1


@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('customer','date_time_shipping')
    list_filter = ('customer','date_time_shipping')


class ShippingInline(admin.TabularInline):
    model = Shipping
    extra=0


class ProductItemInline(admin.TabularInline):
    model = Order.product_items.through
    # fields = ['product', 'quantity']
    extra=0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer')
    inlines = [ShippingInline, ProductItemInline]
    exclude = ('product_items',)


admin.site.register(Basket)
admin.site.register(Image)

