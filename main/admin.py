import json
from payment.models import PaymentData
import requests
from django.contrib import admin, messages
from django.db.models import QuerySet
from .models import *
from modeltranslation.admin import TranslationAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.safestring import mark_safe
from django.utils.html import format_html
import decimal


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('pk', 'title', 'price','new_price', 'wholesale','is_published')
    list_display_links = ('pk', 'title', 'price','new_price', 'wholesale')
    list_filter = ('wholesale', 'category', 'is_published')
    save_on_top = True
    list_editable = ('is_published',)
    search_fields = ('title',)

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('title',)
    prepopulated_fields = {'url': ('title',)}


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    fields = ('customer', 'date_shipping', 'time_shipping', 'payment_type', 'finale_price', 'delivery_cost', 'city', 'address', 'phone', 'comment','status')
    readonly_fields = ('customer', 'date_shipping', 'time_shipping', 'payment_type', 'finale_price', 'delivery_cost', 'city', 'address', 'phone', 'comment','status')


@admin.register(Customer)
class CustomerAdmin(TranslationAdmin):
    list_display = ('user',)
    fields = ('user', 'phone', 'address')
    inlines = [OrderInline, ]
    search_fields = ('user',)


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


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer','date_shipping', 'time_shipping','status_colored', 'pay')
    list_display_links = ('id', 'customer','date_shipping')
    inlines = [ProductItemInline,]
    save_on_top = True
    readonly_fields=('customer','payment_type', 'finale_price', 'delivery_cost', 'date_shipping', 'time_shipping', 'city', 'address', 'phone' )
    fields = ('status','pay','refund','customer','payment_type', 'finale_price', 'delivery_cost', 'date_shipping', 'time_shipping', 'city', 'address', 'phone', 'comment' )
    list_filter = ('customer','status')
    actions = ['cancel_payment', 'refund_payment']

    @admin.action(description='Cancel Payment')
    def cancel_payment(self, request, qs: QuerySet):
        customer=request.user.customer
        current_order = qs.get(customer=customer)
        order = Order.objects.get(customer=customer, id=current_order.id)
        payment = PaymentData.objects.get(user=request.user,order=order)
        url = "https://servicestest.ameriabank.am/VPOS/api/VPOS/CancelPayment"
        print('_______________________')
        print(payment.payment_id)

        payload = json.dumps({
            "PaymentID": payment.payment_id,
            "Username": "3d19541048",
            "Password": "lazY2k"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        cancel_payment_data = requests.request("POST", url, headers=headers, data=payload)
        cancel_payment_data_response = cancel_payment_data.json()
        if cancel_payment_data_response["ResponseCode"] == "00":
            qs.update(pay=Order.CANCEL)
            self.message_user(request, f'Վճարումը հաջողությամբ չեղարկվեց։')
        else:
            self.message_user(request, f'Վճարման չեղարկումը չի հաջողվել։ Փորձեք կրկին։',level=messages.ERROR )

    @admin.action(description='Refund Payment')
    def refund_payment(self, request, qs: QuerySet):
        customer = request.user.customer
        current_order = qs.get(customer=customer)
        order = Order.objects.get(customer=customer, id=current_order.id)
        payment = PaymentData.objects.get(user=request.user, order=order)
        url = "https://servicestest.ameriabank.am/VPOS/api/VPOS/RefundPayment"
        payload = json.dumps({
            "PaymentID": payment.payment_id,
            "Username": "3d19541048",
            "Password": "lazY2k",
            "Amount": decimal.Decimal(order.refund)
        }, cls=DecimalEncoder)
        headers = {
            'Content-Type': 'application/json'
        }
        refund_payment_data = requests.request("POST", url, headers=headers, data=payload)
        refund_payment_data_response = refund_payment_data.json()
        print(refund_payment_data_response)
        print(refund_payment_data_response["ResponseCode"])
        if refund_payment_data_response["ResponseCode"] == "00":
            qs.update(pay=Order.REFUND)
            payment.amount_refund=order.refund
            payment.save()
            self.message_user(request, f'Ետ վերադարձը հաջողությամբ կատարվեց։')
        else:
            self.message_user(request, f'Ետ վերադարձը չի հաջողվել։ Փորձեք կրկին։', level=messages.ERROR)

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
