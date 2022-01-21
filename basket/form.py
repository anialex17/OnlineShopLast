from django import forms

from main.models import Basket, ProductItem, Shipping, Time_Shipping


class AddToBasketForm(forms.ModelForm):
    class Meta:
        model = ProductItem
        fields = ['product', 'quantity']


class ShippingForm(forms.ModelForm):
    time_shipping = forms.ModelChoiceField(queryset=Time_Shipping.objects.all(),
                                           empty_label='Ընտրեք առաքման ժամանակահատնածը',
                                          widget=forms.Select(attrs={'class': "form-control shadow-none"}))
    # payment_type = forms.ModelChoiceField(queryset=Payment_Type.objects.all(),
    #                                        empty_label='Ընտրեք վճարման տարբերակը',
    #                                       widget=forms.Select(attrs={'class': "form-control shadow-none"}))
    class Meta:
        model = Shipping
        fields = ('city', 'address', 'phone', 'date_shipping', 'time_shipping', 'payment_type')
        # fields = '__all__'
        widgets = {
            'city': forms.TextInput(
                attrs={'class': 'form-control shadow-none personal-', 'id': "name", 'placeholder': "Ձեր քաղաքը․․․"}),
            'address': forms.TextInput(attrs={'type': "text", 'class': "form-control shadow-none", 'id': "name",
                                              'placeholder': "Ձեր հասցեն․․․"}),
            'phone': forms.TextInput(attrs={'type': "text", 'class': "form-control shadow-none", 'id': "name",
                                            'placeholder': "+374 ** ******"}),
            'date_shipping': forms.DateInput(
                attrs={'type': "date", 'id': "start", 'class': "date-input", 'name': "trip-start",
                       'value': "2021-12-15", 'min': "2021-12-15", 'max': "2022-12-31"}),
            'time_shipping': forms.Select(attrs={'type': "text", 'class': "form-control shadow-none", 'id': "name",
                                                 'placeholder': "Time"}),
            'payment_type': forms.Select(attrs={'type': "text", 'class': "form-control shadow-none", 'id': "name",
                                                 'placeholder': "Payment type"}),

        }
