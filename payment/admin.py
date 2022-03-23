from django.contrib import admin
from .models import *


@admin.register(PaymentData)
class PaymentDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','order', 'payment_id','response_code')
