from django.db import models


class Payment(models.Model):
    currency_choices = (('051', 'AMD'),('978', 'EUR'), ('840', 'USD'), ('643', 'RUB'))

    client_id = models.CharField(verbose_name='Merchant ID', max_length=255, blank=True, null=True)
    username = models.CharField(verbose_name='Merchant username', max_length=255, blank=True, null=True)
    password = models.CharField(verbose_name='Merchant password', max_length=255, blank=True, null=True)
    currency = models.CharField(verbose_name='Transaction currency', max_length=3, choices=currency_choices, default='AMD', null=True)
    description = models.TextField(verbose_name='Description of the transaction')
    order_id = models.IntegerField(verbose_name='Unique ID of the transaction')
    amount = models.DecimalField(verbose_name='Payment amount', max_digits=10, decimal_places=2)
    back_url = models.CharField(verbose_name='Address on the merchant’s server for returning after payment', max_length=255, blank=True, null=True)
    opaque = models.CharField(verbose_name='Additional data', max_length=255, blank=True, null=True)
    card_holder_id = models.IntegerField(verbose_name='Unique ID for binding transactions', null=True, blank=True)

    def __str__(self):
        return self.description


class PaymentResponse(models.Model):
    payment_id = models.IntegerField()
    response_code = models.CharField(max_length=50)
    response_message = models.TextField()

    def __str__(self):
        return str(self.payment_id)