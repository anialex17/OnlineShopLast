from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin
from django.contrib.contenttypes.admin import GenericTabularInline


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('title', 'price')
    prepopulated_fields = {'url': ('title',)}
    save_on_top = True


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('title',)
    prepopulated_fields = {'url': ('title',)}


@admin.register(Customer)
class CustomerAdmin(TranslationAdmin):
    list_display = ('user',)


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity')
    list_filter = ('customer', 'product')



# class ProductItemInline(admin.TabularInline):
#     model = ProductItem
#     extra = 1


class ProductItemInline(admin.TabularInline):
    model = Order.product_items.through
    extra = 0

#
# class ShippingInline(admin.TabularInline):
#     model = Shipping
#     extra = 1


@admin.register(Shipping)
class ShippingAdmin(TranslationAdmin):
    list_display = ('customer', 'date_shipping', 'time_shipping')
    list_filter = ('customer', 'date_shipping', 'time_shipping')
    readonly_fields = (
    'customer', 'order', 'city', 'address', 'phone', 'date_shipping', 'time_shipping', 'payment_type')


class ShippingInline(admin.TabularInline):
    model = Shipping
    extra = 0
    readonly_fields = ('customer', 'order', 'city', 'address', 'phone', 'date_shipping', 'time_shipping')
    fk_name = 'order'




@admin.register(Order)
class OrderAdmin(TranslationAdmin):
    list_display = ('id', 'customer')
    inlines = [ShippingInline, ProductItemInline]
    exclude = ('product_items',)
    readonly_fields = ('customer', 'product_items', 'date_added', 'finale_price', 'delivery_cost')


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('customer',)


@admin.register(Measurement)
class MeasurementAdmin(TranslationAdmin):
    list_display = ('type',)


admin.site.register(Time_Shipping)
admin.site.register(Image)
