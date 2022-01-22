from modeltranslation.translator import register, TranslationOptions
from main.models import *


@register(Order)
class OrderTranslationOptions(TranslationOptions):
    fields = ('status',)


@register(Shipping)
class ShippingTranslationOptions(TranslationOptions):
    fields = ('city', 'address', 'payment_type')