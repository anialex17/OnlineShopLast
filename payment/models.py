from django.db import models
from django.contrib.auth.models import User
from main.models import Order


class PaymentData(models.Model):
    order = models.OneToOneField(Order,on_delete=models.CASCADE, verbose_name='Պատվերի հերթական համար', blank=True, null=True, related_name='payment_order')
    user = models.ForeignKey(User, verbose_name='Օգտագործող', on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(verbose_name='Գումար', max_digits=10, decimal_places=2, blank=True, null=True)
    # order_id = models.IntegerField(verbose_name='Պատվերի հերթական համար', blank=True, null=True)
    payment_id = models.CharField(max_length=225, verbose_name='Վճարման հերթական համար', blank=True, null=True)
    response_code = models.CharField(max_length=50, verbose_name='Գործառնության պատասխանի կոդ', blank=True, null=True)
    amount_refund = models.DecimalField(verbose_name='Գումար', max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return str(self.user)