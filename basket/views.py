import json
import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from main.forms import RegisterUserForm, LoginUserForm
from main.views import GetContextDataMixin
from main.models import *
from .forms import AddToBasketForm, OrderForm
import uuid
from django.core.mail import send_mail
from payment.models import PaymentData


def basket(request):
    register_form = RegisterUserForm()
    form = LoginUserForm()
    context = {'register_form': register_form, 'form': form}
    if request.user.is_authenticated:
        customer = request.user.customer
        basket = Basket.objects.get(customer_id=customer.id)
        for product_item in basket.productItems.all():
            if product_item.product.is_published == False:
                product_item.delete()
        if basket.finale_price() < 10000:
            basket.delivery_cost = 500
        context = {'basket': basket, 'productItems': basket.productItems.all(), 'register_form': register_form,
                   'form': form}
    else:
        try:
            the_id = request.session['basket_id']
        except:
            basket = Basket(session_key=uuid.uuid4())
            basket.save()
            request.session['basket_id'] = basket.id
            the_id = basket.id
        basket = Basket.objects.get(id=the_id)
        for product_item in basket.productItems.all():
            if product_item.product.is_published == False:
                product_item.delete()
        if basket.finale_price() < 10000:
            basket.delivery_cost = 500
        context = {'basket': basket, 'productItems': basket.productItems.all(), 'register_form': register_form,
                   'form': form}
    return render(request, 'basket/basket.html', context)


def add_to_basket(request):
    form = AddToBasketForm(request.POST)
    if request.method == "POST":
        if request.user.is_authenticated:
            customer = request.user.customer
            product = Product.objects.get(pk=request.POST.get('product_url'))
            product_quantity = request.POST.get('product_quantity').replace(",", ".")
            basket = Basket.objects.get(customer=customer)
            if product.wholesale:
                product_item, created = ProductItem.objects.get_or_create(product=product, customer=customer,
                                                                          wholesale=True, order=None)
            else:
                product_item, created = ProductItem.objects.get_or_create(product=product, customer=customer,
                                                                          order=None)
            product_item.quantity = product_quantity
            basket.productItems.add(product_item)
            product_item.save()
            messages.success(request, 'The product was successfully added to your basket')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            try:
                the_id = request.session['basket_id']
            except:
                basket = Basket(session_key=uuid.uuid4())
                basket.save()
                request.session['basket_id'] = basket.id
                the_id = basket.id
            basket = Basket.objects.get(id=the_id)
            product = Product.objects.get(pk=request.POST.get('product_url'))
            product_quantity = request.POST.get('product_quantity')
            if product.wholesale:
                product_item, created = ProductItem.objects.get_or_create(product=product,
                                                                          session_key=basket.session_key,
                                                                          wholesale=True, order=None)
            else:
                product_item, created = ProductItem.objects.get_or_create(product=product, order=None,
                                                                          session_key=basket.session_key)

            product_item.quantity = product_quantity
            basket.productItems.add(product_item)
            product_item.save()
            messages.add_message(request, messages.INFO, 'The product was successfully added to your basket')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            customer = request.user.customer
            basket = Basket.objects.get(customer=customer)
        else:
            basket = Basket.objects.get(id=request.session['basket_id'])
        product_item = ProductItem.objects.get(pk=request.POST.get('remove_item'))
        basket.productItems.remove(product_item)
        product_item.delete()
        messages.success(request, 'The product is successfully deleted')
    return redirect('basket')


def change_qty_plus(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            customer = request.user.customer
            basket = Basket.objects.get(customer=customer)
        else:
            basket = Basket.objects.get(id=request.session['basket_id'])
        product_item = ProductItem.objects.get(pk=request.POST.get('increment_item'))
        # if product_item and product_item.product.wholesale == False:
        #     product_item.quantity += product_item.product.start_quantity
        # elif product_item and product_item.product.wholesale:
        #     product_item.quantity += 10
        if product_item:
            product_item.quantity += product_item.product.start_quantity
        product_item.save()
        return redirect('basket')


def change_qty_minus(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            customer = request.user.customer
            basket = Basket.objects.get(customer=customer)
        else:
            basket = Basket.objects.get(id=request.session['basket_id'])
        product_item = ProductItem.objects.get(pk=request.POST.get('decrement_item'))
        if product_item:
            product_item.quantity -= product_item.product.start_quantity
            if product_item.quantity < product_item.product.min_order_quantity:
                product_item.delete()
            else:
                product_item.save()
        # elif product_item and product_item.product.wholesale:
        #     product_item.quantity -= 10
        #     if product_item.quantity < product_item.product.min_order_quantity:
        #         product_item.delete()
        #     else:
        #         product_item.save()
        return redirect('basket')


def order(request, *args, **kwargs):
    if request.method == 'POST':
        customer = request.user.customer
        basket = Basket.objects.get(customer=customer)
        form = OrderForm(data=request.POST)
        if form.is_valid():
            if basket.finale_price() > 10000:
                order = Order.objects.create(**form.cleaned_data, customer=customer, basket=basket,
                                             finale_price=basket.finale_price())
            else:
                order = Order.objects.create(**form.cleaned_data, customer=customer, basket=basket,
                                             finale_price=basket.finale_price(), delivery_cost=500)
            customer.orders.add(order)
            for item in basket.productItems.all():
                item.order = order
                if item.product.new_price:
                    item.price = item.product.new_price * item.quantity
                else:
                    item.price = item.product.price * item.quantity
                item.save()
                # order.product_items.add(item)
            if order.payment_type == 'TYPE_PAYMENT_CASH':
                send_mail('Պատվեր',
                          f'Նոր պատվեր-{order.customer.user.first_name} {order.customer.user.last_name}-ի կողմից',
                          'vitamix.company.2022@gmail.com', ['vitamix.company.2022@gmail.com'], fail_silently=False)
                for item in basket.productItems.all():
                    basket.productItems.remove(item)
                return redirect('success')
            elif order.payment_type == 'TYPE_PAYMENT_NON_CASH':
                payment = PaymentData.objects.create(user=request.user, amount=order.finale_price, order_id=order.id)
                url = "https://servicestest.ameriabank.am/VPOS/api/VPOS/InitPayment"
                payload = json.dumps({
                    "ClientID": "01df3a48-3bda-45ea-891c-0667ba982ba4",
                    # "Amount": order.finale_price,
                    "Amount": 10,
                    "OrderID": 2522087,
                    "BackURL": "http://127.0.0.1:8000/hy/payment_response/",
                    "Username": "3d19541048",
                    "Password": "lazY2k",
                    "Description": "Payment"
                })
                headers = {
                    'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                response_data = response.json()
                # print(response2.GET.get('orderID'))
                if response_data['ResponseCode'] == 1:
                    return redirect(
                        f'https://servicestest.ameriabank.am/VPOS/Payments/Pay?id={response_data["PaymentID"]}&lang=am')
                else:
                    return redirect('fail')
    else:
        form = OrderForm()
    return render(request, 'basket/order.html', {'form': form})


def payment_response(request):
    customer = request.user.customer
    orderID = request.GET.get('orderID', '')
    resposneCode = request.GET.get('resposneCode', '')
    paymentID = request.GET.get('paymentID', '')
    basket = Basket.objects.get(customer=customer)
    order = Order.objects.get(basket=basket, id=116)
    payment = PaymentData.objects.get(user=request.user, order=order)
    if resposneCode != '00':
        return redirect('fail')
    url = 'https://servicestest.ameriabank.am/VPOS/api/VPOS/GetPaymentDetails'
    payload = json.dumps({
        "PaymentID": paymentID,
        "Username": "3d19541048",
        "Password": "lazY2k"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    get_payment_detail = requests.request("POST", url, headers=headers, data=payload)
    response_payment_detail = get_payment_detail.json()
    order.pay = 'PAID'
    order.save()
    payment.payment_id = paymentID
    payment.response_code = resposneCode
    payment.order.id = orderID
    payment.save()

    for item in basket.productItems.all():
        basket.productItems.remove(item)
    context = {
        'Amount': response_payment_detail['Amount'],
        'ClientName': response_payment_detail['ClientName'],
        'CardNumber': response_payment_detail['CardNumber'],
    }
    return render(request, 'pages/payment_response.html', context)


def cancel_payment(self, request, **kwargs):
    customer = request.user.customer
    order = Order.objects.get(customer=customer, id=self.kwargs['order_id'])
    print(self.kwargs)
    payment = PaymentData.objects.get(order_id=order.id)
    if order.pay=='CANCEL':
        url = "https://servicestest.ameriabank.am/VPOS/api/VPOS/CancelPayment"
        payload = json.dumps({
            "PaymentID": payment.payment_id,
            "Username": "3d19541048",
            "Password": "lazY2k"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        cancel_payment_data = requests.request("POST", url, headers=headers, data=payload)
        cancel_payment_data_response = cancel_payment_data.json()
        if cancel_payment_data_response["ResponseCode"] == 00:
            return render(request, 'success.html')
        else:
            return redirect('fail')
