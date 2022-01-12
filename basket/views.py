from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
import datetime

from django.views.generic import CreateView, UpdateView
from main.views import GetContextDataMixin
from main.models import *
from .form import AddToBasketForm, ShippingForm


def basket(request):
    context = {}
    if request.user.is_authenticated:
        customer = request.user.customer
        basket = Basket.objects.get(customer_id=customer.id)
        context = {'basket': basket, 'productItems': basket.productItems.all()}
    return render(request, 'basket/basket.html', context)


def add_to_basket(request):
    form = AddToBasketForm(request.POST)

    if request.method == "POST":
        customer = request.user.customer
        product = Product.objects.get(url=request.POST.get('product_url'))
        product_quantity = int(request.POST.get('product_quantity'))
        print(product_quantity)
        basket = Basket.objects.get(customer=customer)
        product_item, created = ProductItem.objects.get_or_create(product=product, customer=customer)
        # product_item = ProductItem.objects.create(product=product, customer=customer)
        # if product_item in basket.productItems.all():
        # if created:
        #     # product_item = ProductItem.objects.get(product=product, customer=customer)
        #     product_item.quantity = + product_quantity
        #     product_item.save()
        # else:
        #     product_item.quantity = product_quantity
        #     basket.productItems.add(product_item)

        if created:
            product_item.quantity = product_quantity
            basket.productItems.add(product_item)
            product_item.save()
        else:
            product_item.quantity = product_quantity
            product_item.save()
    return redirect('basket')


def basket_remove(request):
    if request.method == "POST":
        customer = request.user.customer
        basket = Basket.objects.get(customer=customer)
        product_item = ProductItem.objects.get(pk=request.POST.get('remove_item'))
        basket.productItems.remove(product_item)
        product_item.delete()
        del product_item
    return redirect('basket')


def change_qty_plus(request):
    if request.method == "POST":
        customer = request.user.customer
        basket = Basket.objects.get(customer=customer)
        product_item = ProductItem.objects.get(pk=request.POST.get('increment_item'))
        if product_item:
            product_item.quantity += 1
            product_item.save()
        return redirect('basket')


def change_qty_minus(request):
    if request.method == "POST":
        customer = request.user.customer
        basket = Basket.objects.get(customer=customer)
        product_item = ProductItem.objects.get(pk=request.POST.get('decrement_item'))
        if product_item:
            product_item.quantity -= 1
            if product_item.quantity<=0:
                product_item.delete()
            else:
                product_item.save()
        return redirect('basket')


def order(request):
    context = {}
    if request.user.is_authenticated:
        customer = request.user.customer
        basket = Basket.objects.get(customer=customer)
        # order, created = Order.objects.get_or_create(customer=customer)
        order = Order.objects.create(customer=customer)
        for item in basket.productItems.all():
            order.product_items.add(item)
        form = ShippingForm()
        context = {'order':order, 'form':form}
    return render(request, 'basket/order.html', context)


def shipping(request):
    if request.method =='POST':
        customer = request.user.customer
        order=Order.objects.filter(customer=customer).last()
        form = ShippingForm(data=request.POST)
        if form.is_valid():
            Shipping.objects.create(**form.cleaned_data, customer=customer, order=order)
        return redirect('home')
    else:
        form = ShippingForm()
    return redirect('home')
