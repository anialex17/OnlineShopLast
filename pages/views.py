from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from main.models import *
from main.views import *
from django.core.mail import send_mail


# class SendMessageView(GetContextDataMixin,CreateView):
#     model = SendMessage
#     form_class = ContactForm
#     template_name = 'pages/contact.html'
#     success_url = '/'


def message(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            mail = send_mail(contact_form.cleaned_data['name']+contact_form.cleaned_data['lastname'], contact_form.cleaned_data['message'],contact_form.cleaned_data['email'],
                              ['vitamix.company.2022@gmail.com'], fail_silently=False)
            if mail:
                messages.success(request, 'Նամակը հաջողությամբ ուղարկված է!')
                return redirect('home')
            else:
                messages.error(request, 'Ինչ֊որ բան սխալ է։ Փորձեք կրկին!')
        else:
            messages.error(request, 'Ինչ֊որ բան սխալ է։ Փորձեք կրկին!')

    else:
        contact_form = ContactForm()
    return render(request, 'pages/contact.html', {'contact_form': contact_form})


class ContactView(GetContextDataMixin):
    model = Contact
    template_name = 'pages/contact.html'
    context_object_name = "contacts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_form'] = ContactForm()
        return context


class GalleryView(GetContextDataMixin):
    model = Image
    template_name = 'pages/gallery.html'
    context_object_name = "images"

    def get_queryset(self):
        images = Image.objects.filter(gallery=True)
        return images


class TermsOrderView(GetContextDataMixin):
    model = TermsOrder
    template_name = 'pages/order.html'
    context_object_name = "order"


# def about_us(request):
#     return render(request, 'pages/about-us.html')

class AboutUs(GetContextDataMixin):
    model = TermsOrder
    template_name = 'pages/about-us.html'


class Privacy(GetContextDataMixin):
    model = TermsOrder
    template_name = 'pages/privacy.html'
