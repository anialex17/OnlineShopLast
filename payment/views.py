
from django.shortcuts import render, redirect

from main.models import Basket, Customer, Order


def success(request):
    return render(request, 'payment/success.html')


def fail(request):
    return render(request, 'payment/fail.html')

