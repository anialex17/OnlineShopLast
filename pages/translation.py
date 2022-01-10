from modeltranslation.translator import register, TranslationOptions

from .models import *


@register(TermsOrder)
class TermsOrderTranslationOptions(TranslationOptions):
    fields = ('title','description' )

@register(Contact)
class ContactTranslationOptions(TranslationOptions):
    fields = ('address' ,)