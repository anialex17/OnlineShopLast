from django import forms

from main.models import Basket, ProductItem, Shipping

class AddToBasketForm(forms.ModelForm):
    class Meta:
        model=ProductItem
        fields = ['product', 'quantity']


class ShippingForm(forms.ModelForm):
    class Meta:
        model=Shipping
        # fields = ('city', 'address', 'phone' , 'date_shipping')
        fields = '__all__'
        widgets = {
            'city':forms.TextInput(attrs={'class':'form-control shadow-none personal-','id':"name", 'placeholder':"Ձեր քաղաքը․․․"}),
            'address':forms.TextInput(attrs={'type':"text", 'class':"form-control shadow-none", 'id':"name", 'placeholder':"Ձեր հասցեն․․․"}),
            'phone':forms.TextInput(attrs={'type':"text", 'class':"form-control shadow-none", 'id':"name", 'placeholder':"+374 ** ******"}),
            'date_shipping':forms.DateInput(attrs={'type':"date", 'id':"start", 'class':"date-input", 'name':"trip-start",
                        'value':"2021-12-15",'min':"2021-12-15", 'max':"2022-12-31"}),
        }