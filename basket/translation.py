from modeltranslation.translator import register, TranslationOptions
from main.models import *


@register(ProductItem)
class ProductItemTranslationOptions(TranslationOptions):
    fields = ('customer','product')


@register(Basket)
class BasketTranslationOptions(TranslationOptions):
    fields = ('customer',)


@register(Order)
class OrderTranslationOptions(TranslationOptions):
    fields = ('customer','status' )


@register(Shipping)
class ShippingTranslationOptions(TranslationOptions):
    fields = ('customer', 'order', 'city', 'address', 'payment_type')