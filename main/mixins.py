from django.views import View

from main.models import Customer, Cart


class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        cart = None
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user
                )
            cart = Cart.objects.filter(owner=customer).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        # else:
        #     cart = Cart.objects.filter(for_anonymous_user=True)
        #     if not cart:
        #         cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)



