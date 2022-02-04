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
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            mail = send_mail(form.cleaned_data['name']+form.cleaned_data['lastname'], form.cleaned_data['message'],form.cleaned_data['email'],
                              ['netfornetenyu@gmail.com'], fail_silently=False)
            if mail:
                messages.success(request, 'Ok!!!')
                return redirect('home')
            else:
                messages.error(request, 'Upss!!!')
        else:
            messages.error(request, 'Upss!!!')

    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})



class ContactView(GetContextDataMixin):
    model = Contact
    template_name = 'pages/contact.html'
    context_object_name = "contacts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
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