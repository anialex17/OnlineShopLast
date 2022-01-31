from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import *


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text", 'class': "form-control shadow-none", 'id': "name", 'placeholder': "username"}))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text", 'class': "form-control shadow-none", 'id': "name", 'placeholder': "First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text", 'class': "form-control shadow-none", 'id': "name", 'placeholder': "Last Name"}))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text", 'class': "form-control shadow-none", 'id': "phone", 'placeholder': "Phone number"}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'type': "email", 'class': "form-control shadow-none", 'id': "email", 'placeholder': "Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'type': "password", 'class': "form-control shadow-none", 'id': "password", 'placeholder': "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'type': "password", 'class': "form-control shadow-none", 'id': "password-register_2",
               'placeholder': "Repeat Password"}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'type': "text", 'class': "form-control shadow-none", 'id': "name", 'placeholder': "Name"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'type': "password", 'class': "form-control shadow-none", 'id': "password", 'placeholder': "Password"}))


class EditUserForm(UserChangeForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Your First Name', 'id': 'formGroupExampleInput2'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Your Last Name', 'id': 'formGroupExampleInput2'}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Your username', 'id': 'formGroupExampleInput2'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('phone', 'address')
        widgets = {
            'phone':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Your phone' }),
            'address':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Your address'})
        }


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = ('phone', 'address')


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=100,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=100,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=100,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
