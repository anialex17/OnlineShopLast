from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Measurement)
class MeasurementTranslationOptions(TranslationOptions):
    fields = ('type',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('category','title', 'description','measurement')


@register(Image)
class ImageTranslationOptions(TranslationOptions):
    fields = ('product',)


@register(Customer)
class CustomerTranslationOptions(TranslationOptions):
    fields = ('user','address', )


