from django.shortcuts import render
from django.views import View
from django.db import transaction

from main.models import Basket, Customer, Order


def success(request):
    return render(request, 'payment/success.html')


def fail(request):
    return render(request, 'payment/fail.html')


def payment(request):
    customer = Customer.objects.get(user=request.user)
    basket = Basket.objects.get(customer=customer)
    return render(request, 'payment/payment.html', {'basket': basket})


# class PayedOnlineOrderView(View):
#
#     @transaction.atomeic
#     def post(self, request, *args, **kwargs):
#         customer = Customer.objects.get(user=request.user)
#         new_order = Order()
#         new_order.customer = customer


