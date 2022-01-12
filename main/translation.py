from modeltranslation.translator import register, TranslationOptions

from .models import *


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'category', 'description', 'product_type')


@register(Customer)
class CustomerTranslationOptions(TranslationOptions):
    fields = ('address',)
