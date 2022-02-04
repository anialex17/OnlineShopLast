from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
import datetime

from django.views.generic import CreateView, UpdateView

from main.forms import RegisterUserForm, LoginUserForm
from main.views import GetContextDataMixin
from main.models import *
from .forms import AddToBasketForm, OrderForm


def basket(request):
    register_form = RegisterUserForm()
    form = LoginUserForm()
    context = {'register_form':register_form, 'form':form}
    if request.user.is_authenticated:
        customer = request.user.customer
        basket = Basket.objects.get(customer_id=customer.id)
        if basket.finale_price() < 10000:
            basket.delivery_cost = 500
        context = {'basket': basket, 'productItems': basket.productItems.all(),'register_form':register_form, 'form':form }
    return render(request, 'basket/basket.html', context)


def add_to_basket(request):
    form = AddToBasketForm(request.POST)

    if request.method == "POST":
        customer = request.user.customer
        product = Product.objects.get(pk=request.POST.get('product_url'))
        product_quantity = request.POST.get('product_quantity')
        basket = Basket.objects.get(customer=customer)
        if product.wholesale:
            product_item, created = ProductItem.objects.get_or_create(product=product, customer=customer, wholesale=True)
        else:
            product_item, created = ProductItem.objects.get_or_create(product=product, customer=customer)
        if created:
            product_item.quantity = product_quantity
            basket.productItems.add(product_item)
            product_item.save()
            messages.success(request, 'The product is successfully added to your basket')
            # messages.add_message(request, messages.INFO, 'The product is successfully added to your basket')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            product_item.quantity = product_quantity
            product_item.save()
            messages.add_message(request, messages.INFO, 'The product is successfully added to your basket')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
            # return redirect('home')




def basket_remove(request):
    if request.method == "POST":
        customer = request.user.customer
        basket = Basket.objects.get(customer=customer)
        product_item = ProductItem.objects.get(pk=request.POST.get('remove_item'))
        basket.productItems.remove(product_item)
        product_item.delete()
        del product_item
        messages.success(request, 'The product is successfully deleted')
        # messages.add_message(request, messages.INFO, 'The product is successfully deleted')
        # return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return redirect('basket')


def change_qty_plus(request):
    if request.method == "POST":
        customer = request.user.customer
        basket = Basket.objects.get(customer=customer)
        product_item = ProductItem.objects.get(pk=request.POST.get('increment_item'))
        if product_item and product_item.product.wholesale==False:
            product_item.quantity += product_item.product.start_quantity
        elif product_item and product_item.product.wholesale:
            product_item.quantity += 10
        product_item.save()
        return redirect('basket')


def change_qty_minus(request):
    if request.method == "POST":
        customer = request.user.customer
        basket = Basket.objects.get(customer=customer)
        product_item = ProductItem.objects.get(pk=request.POST.get('decrement_item'))
        if product_item and product_item.product.wholesale==False:
            product_item.quantity -= product_item.product.start_quantity
            if product_item.quantity <= 0:
                product_item.delete()
            else:
                product_item.save()
        elif product_item and product_item.product.wholesale:
            product_item.quantity -= 10
            if product_item.quantity < product_item.product.min_order_quantity:
                product_item.delete()
            else:
                product_item.save()
        return redirect('basket')


def order(request):
    if request.method =='POST':
        customer = request.user.customer
        basket = Basket.objects.get(customer=customer)
        form = OrderForm(data=request.POST)
        if form.is_valid():
            if basket.finale_price() > 10000:
                order = Order.objects.create(**form.cleaned_data,customer=customer,basket=basket, finale_price=basket.finale_price())
            else:
                order = Order.objects.create(**form.cleaned_data,customer=customer,basket=basket, finale_price=basket.finale_price(), delivery_cost=500)
            for item in basket.productItems.all():
                order.product_items.add(item)
            if order.payment_type=='TYPE_PAYMENT_NON_CASH':
                return redirect('payment')
            elif order.payment_type=='TYPE_PAYMENT_CASH':
                return redirect('success')

    else:
        form = OrderForm()
    return render(request, 'basket/order.html', {'form':form})

# def order(request):
#     if request.method =='POST':
#         customer = request.user.customer
#         basket = Basket.objects.get(customer=customer)
#         form = ShippingForm(data=request.POST)
#         if form.is_valid():
#             if basket.finale_price() > 10000:
#                 order = Order.objects.create(customer=customer, finale_price=basket.finale_price())
#             else:
#                 order = Order.objects.create(customer=customer, finale_price=basket.finale_price(), delivery_cost=500)
#             for item in basket.productItems.all():
#                 order.product_items.add(item)
#             shipping=Shipping.objects.create(**form.cleaned_data, customer=customer, order=order)
#             if shipping.payment_type=='TYPE_PAYMENT_NON_CASH':
#                 return redirect('basket')
#             elif shipping.payment_type=='TYPE_PAYMENT_CASH':
#                 return redirect('home')
#     else:
#         form = ShippingForm()
#     return render(request, 'basket/order.html', {'form':form})




# def order(request):
#     context = {}
#     if request.user.is_authenticated:
#         customer = request.user.customer
#         basket = Basket.objects.get(customer=customer)
#         if basket.finale_price()>10000:
#             order = Order.objects.create(customer=customer, finale_price=basket.finale_price())
#         else:
#             order = Order.objects.create(customer=customer, finale_price=basket.finale_price(), delivery_cost=500)
#
#     for item in basket.productItems.all():
#         order.product_items.add(item)
#         form = ShippingForm()
#         context = {'order':order, 'form':form}
#     return render(request, 'basket/order.html', context)
# #
#
# def shipping(request):
#     if request.method =='POST':
#         customer = request.user.customer
#         order=Order.objects.filter(customer=customer).last()
#         print(order)
#         form = ShippingForm(data=request.POST)
#         if form.is_valid():
#             Shipping.objects.create(**form.cleaned_data, customer=customer, order=order)
#         return redirect('home')
#     else:
#         form = ShippingForm()
#     return redirect('home')
#






