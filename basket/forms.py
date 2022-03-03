from django import forms
from datetime import date
from main.models import Basket, ProductItem, Order, Time_Shipping
import datetime

class AddToBasketForm(forms.ModelForm):
    class Meta:
        model = ProductItem
        fields = ['product', 'quantity']


class OrderForm(forms.ModelForm):
    time_shipping = forms.ModelChoiceField(queryset=Time_Shipping.objects.all(),
                                           empty_label='Ընտրեք առաքման ժամանակահատնածը',
                                          widget=forms.Select(attrs={'class': "form-control shadow-none"}))
    # payment_type = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control shadow-none"}))

    class Meta:
        model = Order
        fields = ('city', 'address', 'phone', 'date_shipping', 'time_shipping', 'payment_type', 'comment')
        # fields = '__all__'
        widgets = {
            'city': forms.TextInput(
                attrs={'class': 'form-control shadow-none personal-', 'id': "name", 'placeholder': "Ձեր քաղաքը․․․"}),
            'address': forms.TextInput(attrs={'type': "text", 'class': "form-control shadow-none", 'id': "name",
                                              'placeholder': "Ձեր հասցեն․․․"}),
            'phone': forms.TextInput(attrs={'type': "text", 'class': "form-control shadow-none", 'id': "name",
                                            'placeholder': "+374 ** ******"}),
            'date_shipping': forms.DateInput(
                attrs={'type': "date", 'id': "start", 'class': "date-input", 'name': "trip-start", 'min':date.today(),
                       'max':date.today()+datetime.timedelta(days=1)}),
            'time_shipping': forms.Select(attrs={'type': "text", 'class': "form-control shadow-none", 'id': "name",
                                                 'placeholder': "Time"}),
            'payment_type': forms.Select(attrs={'type': "text", 'class': "form-control shadow-none", 'id': "name",
                                                 'placeholder': "Payment type"}),
            'comment': forms.TextInput(attrs={'type': "text", 'class': "form-control shadow-none", 'id': "name",
                                              'placeholder': "Ձեր մեկնաբանությունը․․․"}),
        }