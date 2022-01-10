from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import ListView, UpdateView, DetailView, CreateView
from .email import send_activate_mail
from .forms import *


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
    paginate_by = 6


class ProductListView(ListView):
    model = Product
    template_name = 'main/menu.html'
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(category__url=self.kwargs.get("category_slug")).select_related('category')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product.html'
    context_object_name = "product"
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(category__url=self.kwargs.get("category_slug"))
        context['product_item'] = Product.objects.filter(url=self.kwargs.get("slug")).first()
        context['register_form'] = RegisterUserForm()
        context['form'] = LoginUserForm()
        return context


def register(request):
    if request.method == 'POST':
        register_form = RegisterUserForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            print('register_form.is_valid')
            import time
            customer = Customer.objects.create(user=user)
            Basket.objects.create(customer=customer)
            # url = str(round(time.time() * 1000))
            send_activate_mail(request=request, user=user)
            # login(request, user)
            messages.success(request, 'send_activate_mail Ok!!!')
            return redirect('home')
        else:
            print(register_form.errors())

            # return redirect(request.META.get('HTTP_REFERER'))
            return redirect('home')
    else:
        register_form = RegisterUserForm(request.POST)
        messages.error(request, 'some error message here')
    return render(request, 'include/header.html', {'register_form': register_form})


def user_login(request):
    print(request.user.pk)
    if request.method == 'POST':
        context = {'data': request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        # if user and not user.is_email_verified:
        #     messages.add_message(request, messages.ERROR,
        #                          'Email is not verified, please check your email inbox')
        #     return redirect(request.META.get('HTTP_REFERER'))

        # if not user:
        #     messages.add_message(request, messages.ERROR,
        #                          'Invalid credentials, try again')
        #     return redirect(request.META.get('HTTP_REFERER'))

        login(request, user)

        messages.add_message(request, messages.SUCCESS,
                             f'Welcome {user.username}')

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
    form = EditCustomerForm(initial={
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': customer.phone,
    })
    context = {'customer': customer,
               'form': form,
               'orders':orders,
               }
    return render(request, 'main/customer.html', context)


#
#
# def edit_profile(request):
#
#     if request.method == 'POST':
#         form = EditCustomerForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)  # request.FILES is show the selected image or file
#
#         if form.is_valid():
#             user_form = form.save()
#             custom_form = profile_form.save(False)
#             custom_form.user = user_form
#             custom_form.save()
#             return redirect('accounts:view_profile')
#     else:
#         form = EditProfileForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.userprofile)
#         args = {}
#         # args.update(csrf(request))
#         args['form'] = form
#         args['profile_form'] = profile_form
#         return render(request, 'main/customer.html', args)

# def edit_user(request):
#     if request.method=='POST':
#         form = EditCustomerForm(data=request.POST)
#         if form.is_valid():
#             customer= Customer.objects.update(self, {username:form.username,})


class UserEditView(UpdateView):
    form_class = EditCustomerForm
    template_name = 'main/customer.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

    # def form_valid(self, form):
    #     user = self.request.user
    #     user.username = form.cleaned_data.get('username')
    #     user.first_name = form.cleaned_data.get('first_name')
    #     user.last_name = form.cleaned_data.get('last_name')
    #     # user.phone = form.cleaned_data.get('phone')
    #     user.save()
    #     return redirect(self.request.META.get('HTTP_REFERER'))


# class PasswordsChangeView(PasswordChangeView):
#     form_class = PasswordChangingForm
#     success_url = reverse_lazy('/')

# def form_valid(self, form):
#     user = self.request.user
#     user.old_password = form.cleaned_data.get('old_password')
#     user.new_password1 = form.cleaned_data.get('new_password1')
#     user.new_password2 = form.cleaned_data.get('new_password2')
#
#     user.save()
#     return redirect(self.request.META.get('HTTP_REFERER'))
#
# def get_form_kwargs(self):
#     kwargs = super().get_form_kwargs()
#     kwargs['user'] = self.request.user
#     return kwargs


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')


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
