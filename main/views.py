from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import login, logout, authenticate, views
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, BadHeaderError, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django import views
from django.views import View
from django.views.generic import ListView, UpdateView, DetailView, CreateView
from .email import send_activate_mail
from django.db.models import Count, F, Q
from .forms import *
from .models import *
import uuid
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes




class GetContextDataMixin(ListView):

    def get_context_data(self,**kwargs):
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


class ProductListView(GetContextDataMixin):
    model = Product
    template_name = 'main/menu.html'
    context_object_name = "products"
#     paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(category__url=self.kwargs.get("category_slug"),wholesale=False).select_related('category','measurement')


class ProductWholeSaleListView(GetContextDataMixin):
    model = Product
    template_name = 'main/menu.html'
    context_object_name = "products"
#     paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(category__url=self.kwargs.get("category_slug"), wholesale=True).select_related('category', 'measurement')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product.html'
    context_object_name = "product"
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_item'] = Product.objects.get(pk=self.kwargs.get("pk"))
        if context['product_item'].wholesale:
            context['products'] = Product.objects.filter(category__url=self.kwargs.get("category_slug"), wholesale=True).select_related('category', 'measurement')[:5]
        else:
            context['products'] = Product.objects.filter(category__url=self.kwargs.get("category_slug"), wholesale=False).select_related('category', 'measurement')[:5]
        context['register_form'] = RegisterUserForm()
        context['form'] = LoginUserForm()
        return context


def register(request):
    if request.method == 'POST':
        register_form = RegisterUserForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            email = register_form.cleaned_data.get('email')
            if User.objects.filter(email=email):
                messages.warning(request, 'This email is already in use!')
                return redirect('home')
            else:
                send_activate_mail(request=request, user=user)
            customer = Customer.objects.create(user=user, phone=register_form.cleaned_data['phone'])
            Basket.objects.create(customer=customer)
            # url = str(round(time.time() * 1000))
            # send_activate_mail(request=request, user=user)
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


def user_login(request):
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            context = {'data': request.POST}
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            if request.session.get('basket_id'):
                basket = Basket.objects.get(id=request.session['basket_id'])
                customer = Customer.objects.get(user=request.user)
                customer_basket = Basket.objects.filter(customer=customer).first()
                for item in basket.productItems.all():
                    item.session_key=None
                    item.customer=customer
                    item.save()
                    for i in customer_basket.productItems.all():
                        if item.product==i.product:
                            i.quantity=item.quantity
                            i.save()
                            item.delete()
                            break
                    else:
                        customer_basket.productItems.add(item)
                basket.session_key = None
                basket.delete()
                customer_basket.save()
                messages.add_message(request, messages.SUCCESS,f'Welcome {user.first_name} {user.last_name}')
                return redirect(reverse('home'))
            else:
                messages.add_message(request, messages.SUCCESS,f'Welcome {user.first_name} {user.last_name}')
                return redirect(reverse('home'))
        else:
            form = LoginUserForm(request.POST or None)
            messages.add_message(request, messages.WARNING,'Something is wrong. Try again!')
            return redirect(reverse('home'))
    return render(request, 'include/header.html')


# def user_login(request):
#     if request.method == 'POST':
#         context = {'data': request.POST}
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(request, username=username, password=password)
#         login(request, user)
#         if request.session.get('basket_id'):
#             basket = Basket.objects.get(id=request.session['basket_id'])
#             customer = Customer.objects.get(user=request.user)
#             customer_basket = Basket.objects.filter(customer=customer).first()
#             for item in basket.productItems.all():
#                 item.session_key=None
#                 item.customer=customer
#                 item.save()
#                 for i in customer_basket.productItems.all():
#                     if item.product==i.product:
#                         i.quantity=item.quantity
#                         i.save()
#                         item.delete()
#                         break
#                 else:
#                     customer_basket.productItems.add(item)
#             basket.session_key = None
#             # basket.delete()
#             customer_basket.save()
#
#         messages.add_message(request, messages.SUCCESS,f'Welcome {user.username}')
#         return redirect(reverse('home'))
#
#     return render(request, 'include/header.html')


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


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/email_password_reset.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="main/password_reset.html", context={"password_reset_form":password_reset_form})
