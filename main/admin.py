from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin
from django.contrib.contenttypes.admin import GenericTabularInline


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
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
    readonly_fields = ('product',)

class ProductItemInline(admin.TabularInline):
    model = ProductItem
    extra=1

#
# class ShippingInline(admin.TabularInline):
#     model = Shipping
#     extra = 1


@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('customer','date_shipping','time_shipping' )
    list_filter = ('customer','date_shipping', 'time_shipping')
    readonly_fields = ('customer', 'order', 'city', 'address', 'phone', 'date_shipping', 'time_shipping')


class ShippingInline(admin.TabularInline):
    model = Shipping
    extra=0
    readonly_fields = ('customer', 'order', 'city', 'address', 'phone', 'date_shipping', 'time_shipping')


class ProductItemInline(admin.TabularInline):
    model = Order.product_items.through
    extra=0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer')
    inlines = [ShippingInline, ProductItemInline]
    exclude = ('product_items',)
    readonly_fields = ('customer','product_items','date_added', 'finale_price','delivery_cost' )



admin.site.register(Basket)
admin.site.register(Image)
# admin.site.register(Measurement)
admin.site.register(Time_Shipping)

