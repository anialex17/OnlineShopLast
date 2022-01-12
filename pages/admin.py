from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


@admin.register(TermsOrder)
class TermsOrderAdmin(TranslationAdmin):
    list_display = ('title',)


@admin.register(Contact)
class ContactAdmin(TranslationAdmin):
    list_display = ('address',)


admin.site.register(SendMessage)




