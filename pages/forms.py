from django import forms
from .models import *


class ContactForm(forms.ModelForm):

    class Meta:
        model = SendMessage
        fields = ['name', 'lastname', 'email', 'message', 'file']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'name', 'type':"text", 'class':"form-control shadow-none", 'id':"name_contact"}),
            'lastname': forms.TextInput(attrs={'placeholder': 'lastname','type':"text", 'class':"form-control shadow-none", 'id':"lastname_contact" }),
            'email': forms.EmailInput(attrs={'placeholder': 'email','type':"email",'class':"form-control shadow-none", 'id':"email_contact"}),
            'message': forms.Textarea(attrs={'placeholder': 'message','id':"exampleFormControlTextarea1", 'rows':"3",'class':"form-control shadow-none"}),
            'file': forms.FileInput(attrs={'placeholder': 'file','type':"file", 'name':"file", 'class':"file_input d-none"})

        }