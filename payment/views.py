from django.shortcuts import render


def success(request):
    return render(request, 'basket/success.html')


def fail(request):
    return render(request, 'basket/fail.html')

def payment(request):
    return render(request, 'basket/payment.html')