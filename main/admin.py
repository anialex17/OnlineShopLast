from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin
from django.contrib.contenttypes.admin import GenericTabularInline


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('pk', 'title', 'price', 'wholesale')
    # prepopulated_fields = {'url': ('title',)}
    list_filter = ('wholesale',)
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
    list_display = ('id', 'customer', 'product', 'quantity')
    list_filter = ('customer', 'product')


class ProductItemInline(admin.TabularInline):
    model = Order.product_items.through
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer','date_shipping','status')
    list_display_links = ('id', 'customer','date_shipping','status')
    inlines = [ProductItemInline]
    # exclude = ('product_items',)
    readonly_fields=('customer','payment_type', 'finale_price', 'delivery_cost','product_items', 'date_shipping', 'time_shipping', 'city', 'address', 'phone' )
    fields = ('status','customer','payment_type', 'finale_price', 'delivery_cost','product_items', 'date_shipping', 'time_shipping', 'city', 'address', 'phone' )



@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('customer',)


@admin.register(Measurement)
class MeasurementAdmin(TranslationAdmin):
    list_display = ('type',)


admin.site.register(Time_Shipping)
admin.site.register(Image)
