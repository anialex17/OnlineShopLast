from django.contrib import messages
from django.contrib.sites import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from main.forms import RegisterUserForm, LoginUserForm
from main.views import GetContextDataMixin
from main.models import *
from payment.forms import PaymentForm, PaymentResponseForm
from payment.models import Payment, PaymentResponse
from .forms import AddToBasketForm, OrderForm
import uuid
from django.core.mail import send_mail


def basket(request):
    register_form = RegisterUserForm()
    form = LoginUserForm()
    context = {'register_form': register_form, 'form': form}
    if request.user.is_authenticated:
        customer = request.user.customer
        basket = Basket.objects.get(customer_id=customer.id)
        for product_item in basket.productItems.all():
            if product_item.product.is_published==False:
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
            if product_item.product.is_published==False:
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


def order(request):
    form = PaymentForm()
    form_response = PaymentResponseForm()
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
            for item in basket.productItems.all():
                item.order = order
                if item.product.new_price:
                    item.price=item.product.new_price*item.quantity
                else:
                    item.price = item.product.price*item.quantity
                item.save()
                basket.productItems.remove(item)
                # order.product_items.add(item)
            if order.payment_type == 'TYPE_PAYMENT_NON_CASH':
                # send_mail('Պատվեր',f'Նոր պատվեր-{order.customer.user.first_name} {order.customer.user.last_name}-ի կողմից', 'netfornetenyu@gmail.com', ['netfornetenyu@gmail.com'], fail_silently=False)
                # return redirect('payment')
                payment = Payment.objects.create(description=f'online payment {request.user.first_name}',
                                                 order_id=order.id,
                                                 amount=basket.finale_price)
                # payment = PaymentForm(description=f'online payment {request.user.first_name}',
                #                                  order_id=order.id,
                #                                  amount=basket.finale_price)
                data = {payment.description: f'online payment {request.user.first_name}', payment.order_id: order.id,
                        payment.amount: basket.finale_price()}
                payment_request = requests.post('https://servicestest.ameriabank.am/VPOS/api/VPOS/InitPayment', data=data)
                payment_response = PaymentResponse.objects.create(payment_id=payment_request.payment_id,
                                                                   response_code=payment_request.response_code,
                                                                   response_message=payment_request.response_message)

                return redirect(f'https://servicestest.ameriabank.am/VPOS/Payments/Pay ? id =@ id & lang =@lang')
            elif order.payment_type == 'TYPE_PAYMENT_CASH':
                send_mail('Պատվեր',f'Նոր պատվեր-{order.customer.user.first_name} {order.customer.user.last_name}-ի կողմից',
                          'netfornetenyu@gmail.com', ['netfornetenyu@gmail.com'], fail_silently=False)
                return redirect('success')
    else:
        form = OrderForm()
    return render(request, 'basket/order.html', {'form': form})



