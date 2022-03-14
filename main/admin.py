from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.safestring import mark_safe
from django.utils.html import format_html


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('pk', 'title', 'price','new_price', 'wholesale','is_published')
    list_display_links = ('pk', 'title', 'price','new_price', 'wholesale')
    list_filter = ('wholesale', 'category', 'is_published')
    save_on_top = True
    list_editable = ('is_published',)


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('title',)
    prepopulated_fields = {'url': ('title',)}


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    fields = ('customer', 'date_shipping', 'time_shipping','payment_type', 'finale_price', 'delivery_cost', 'city', 'address', 'phone', 'comment','status')
    readonly_fields = ('customer', 'date_shipping', 'time_shipping','payment_type', 'finale_price', 'delivery_cost', 'city', 'address', 'phone', 'comment','status')


@admin.register(Customer)
class CustomerAdmin(TranslationAdmin):
    list_display = ('user',)
    fields = ('user', 'phone','address')
    inlines = [OrderInline,]


# @admin.register(ProductItem)
# class ProductItemAdmin(admin.ModelAdmin):
#     list_display = ['id', 'customer', 'product', 'quantity', 'price','total_price', 'order']
#     list_filter = ('customer', 'product', 'order')
#     fields = ('customer', 'product','quantity', 'wholesale','price', 'total_price', 'order')
#     readonly_fields = ('customer', 'product','quantity', 'wholesale','total_price','price', 'order')


# class ProductItemInline(admin.TabularInline):
#     model = Order.product_items.through
#     extra = 0


class ProductItemInline(admin.TabularInline):
    model = ProductItem
    extra = 0
    fields = ('customer', 'product', 'wholesale', 'quantity','get_measurement','price', 'order')
    readonly_fields = ('customer', 'product','quantity', 'get_measurement','price', 'wholesale', 'order')

    def get_measurement(self, object):
        return object.product.measurement

    # def get_price(self, object):
    #     if object.product.new_price:
    #         return object.product.new_price * object.quantity
    #     else:
    #         return object.product.price * object.quantity

    get_measurement.short_description = "Չափման միավոր"
    # get_price.short_description = "Ընդհանուր գումար"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer','date_shipping', 'time_shipping','status_colored')
    list_display_links = ('id', 'customer','date_shipping')
    inlines = [ProductItemInline,]
    save_on_top = True
    readonly_fields=('customer','payment_type', 'finale_price', 'delivery_cost', 'date_shipping', 'time_shipping', 'city', 'address', 'phone' )
    fields = ('status','customer','payment_type', 'finale_price', 'delivery_cost', 'date_shipping', 'time_shipping', 'city', 'address', 'phone', 'comment' )
    list_filter = ('customer','status')

    def status_colored(self, obj):
        if obj.status=='STATUS_READY':
            return mark_safe('<b style="background:{};">{}</b>'.format('orange', 'Պատվերը պատրաստ է'))
        elif obj.status=='STATUS_COMPLETED':
            return mark_safe('<b style="background:{};">{}</b>'.format('green', 'Պատվերը առաքված է'))
        elif obj.status=='STATUS_NEW':
            return mark_safe('<b style="background:{};">{}</b>'.format('red', 'Նոր պատվեր'))

    status_colored.short_description = 'Ստատուս'

# @admin.register(Basket)
# class BasketAdmin(admin.ModelAdmin):
#     list_display = ('id','customer','session_key')


@admin.register(Measurement)
class MeasurementAdmin(TranslationAdmin):
    list_display = ('type',)


admin.site.register(Time_Shipping)
# admin.site.register(Image)
