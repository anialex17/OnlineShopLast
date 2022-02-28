import requests
from django.shortcuts import render, redirect
from django.views import View
from django.db import transaction
from .models import Payment
from .forms import PaymentForm, PaymentResponseForm
from main.models import Basket, Customer, Order


def success(request):
    return render(request, 'payment/success.html')


def fail(request):
    return render(request, 'payment/fail.html')


def payment(request):
    form = PaymentForm()
    form_response = PaymentResponseForm()
    customer = Customer.objects.get(user=request.user)
    basket = Basket.objects.get(customer=customer)
    # order = Order.objects.get(basket=basket)
    # if request.method == 'POST':
    #     url = 'https://servicestest.ameriabank.am/VPOS/api/VPOS/InitPayment'
    #     data = {'client_id': 1, 'username': 'username', 'password': 'password', 'description': 'description',
    #             'order_id': order.id, 'amount': basket.finale_price}
    #     request = requests.post(url, data)
    #     form = PaymentForm(data)
    #     form.save()
    #     redirect_url = requests.get(f'https://servicestest.ameriabank.am/VPOS/Payments/Pay ? id =@id & lang =@lang')
    #     return redirect(redirect_url)
    return render(request, 'payment/payment.html', {'basket': basket})

# class PayedOnlineOrderView(View):
#
#     @transaction.atomeic
#     def post(self, request, *args, **kwargs):
#         customer = Customer.objects.get(user=request.user)
#         new_order = Order()
#         new_order.customer = customer
