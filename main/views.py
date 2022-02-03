from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import login, logout, authenticate, views
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django import views
from django.views import View
from django.views.generic import ListView, UpdateView, DetailView, CreateView
from .email import send_activate_mail
from django.db.models import Count, F
from .forms import *
from .models import *


class GetContextDataMixin(ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['register_form'] = RegisterUserForm()
        context['form'] = LoginUserForm()
        return context


class HomeView(GetContextDataMixin):
    model = Category
    template_name = 'main/home.html'
    context_object_name = 'categories'
    queryset = Category.objects.annotate(cnt=Count('product')).filter(product__wholesale=False).filter(cnt__gt=0)


class WholeSaleView(GetContextDataMixin):
    model = Category
    template_name = 'main/wholesale.html'
    context_object_name = 'categories'
    queryset = Category.objects.annotate(cnt=Count('product', filter=F('product__wholesale'))).filter(cnt__gt=0)


class ProductListView(ListView):
    model = Product
    template_name = 'main/menu.html'
    context_object_name = "products"
#     paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(category__url=self.kwargs.get("category_slug"),wholesale=False).select_related('category')


class ProductWholeSaleListView(ListView):
    model = Product
    template_name = 'main/menu.html'
    context_object_name = "products"
#     paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(category__url=self.kwargs.get("category_slug"), wholesale=True).select_related('category')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product.html'
    context_object_name = "product"
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(category__url=self.kwargs.get("category_slug")).select_related('category')
        # context['product_item'] = Product.objects.filter(url=self.kwargs.get("slug")).first()
        context['product_item'] = Product.objects.get(pk=self.kwargs.get("pk"))
        context['register_form'] = RegisterUserForm()
        context['form'] = LoginUserForm()
        return context


def register(request):
    if request.method == 'POST':
        register_form = RegisterUserForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            import time
            customer = Customer.objects.create(user=user, phone=register_form.cleaned_data['phone'])
            Basket.objects.create(customer=customer)
            # url = str(round(time.time() * 1000))
            send_activate_mail(request=request, user=user)
            # login(request, user)
            messages.success(request, 'Activate code has been sent successfully!!!')
            return redirect('home')
        else:
            register_form = RegisterUserForm(request.POST)
            print(register_form.errors)
            messages.error(request, 'Something is wrong. Try again!')
            return redirect(request.META.get('HTTP_REFERER'))

    else:
        register_form = RegisterUserForm(request.POST)
        messages.error(request, 'some error message here')
    return render(request, 'include/header.html', {'register_form': register_form})


# class LoginView(views.View):
#
#     def get(self, request, *args, **kwargs):
#         form = LoginUserForm(request.POST or None)
#         print(form)
#         print(request.POST)
#         context = {'form':form}
#         return redirect(reverse('home'))
#
#     def post(self, request, *args, **kwargs):
#         form = LoginUserForm(request.POST or None)
#         if form.is_valid():
#             context = {'data': request.POST}
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user= authenticate(request, username=username, password=password)
#             login(request, user)
#             return redirect(reverse('home'))
#         context = {
#             'form':form
#         }
#         return redirect(reverse('home'))


def user_login(request):
    if request.method == 'POST':
        context = {'data': request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        login(request, user)
        messages.add_message(request, messages.SUCCESS,f'Welcome {user.username}')
        return redirect(reverse('home'))

    return render(request, 'include/header.html')


    # if request.method == 'POST':
    #     context = {'data': request.POST}
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     user = authenticate(request, username=username, password=password)
    #     form = LoginUserForm(data=request.POST)
    #     if form.is_valid():
    #         user = form.get_user()
    #         # if not user.is_email_verifited:
    #         #     messages.add_message(request, messages.ERROR,'Email is not verified, please check your email inbox')
    #         #     return render(request, 'include/header.html', {'form': form}, status=401)
    #         login(request, user)
    #         return redirect('home')
    #
    #     else:
    #         form.errors
    #         return redirect('home')
    #
    # else:
    #     form = LoginUserForm()
    #     return redirect('home')
    #
    # return render(request, 'include/header.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('home')


def customer(request, pk):
    customer = Customer.objects.get(user=request.user)
    orders = Order.objects.filter(customer=customer)
    user_form = EditUserForm(initial={
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    })
    customer_form = EditCustomerForm(initial={
        'phone':customer.phone,
        'address':customer.address
    })
    context = {'customer': customer,
               'user_form': user_form,
               'customer_form':customer_form,
               'orders':orders,
               }
    return render(request, 'main/customer.html', context)


def edit_profile(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        customer_form = EditCustomerForm(request.POST, instance=customer)
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            # messages.success(request, 'Your profile is updated successfully')
            return redirect('profile', request.user.id )
    else:
        user_form = EditUserForm(instance=request.user)
        customer_form = EditCustomerForm(instance=customer)

    return redirect('profile', request.user.id )


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')
    template_name = 'main/password_change.html'


def password_success(request):
    return render(request, 'main/password_success.html', {})


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Account successfully activated!')
            return redirect('home')
        else:
            messages.success(request, 'Activation link is invalid!')
            return redirect('home')