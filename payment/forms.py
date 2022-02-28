from django import forms
from .models import Payment, PaymentResponse


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentResponseForm(forms.ModelForm):
    class Meta:
        model = PaymentResponse
        fields = '__all__'