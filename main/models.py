from django.utils import timezone
import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
# User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=250, verbose_name='Կատեգորիա')
    image = models.ImageField(upload_to='photos', verbose_name="Նկար")
    url = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Կաեգորիա'
        verbose_name_plural = 'Կատեգորիաներ'
        ordering = ['id']

    def __str__(self):
        return self.title


class Measurement(models.Model):
    type = models.CharField(max_length=50, verbose_name='Չափման միավոր')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Չափման միավոր'
        verbose_name_plural = 'Չափման միավորներ'


class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Կատեգորիա', null=True, blank=True, db_constraint=False)
    title = models.CharField(max_length=255, verbose_name='Անուն')
    image = models.ImageField(upload_to='media', null=True, blank=True, verbose_name='Նկար')
    description = models.TextField(verbose_name='Նկարագրություն')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Գին')
    new_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='Նոր գին')
    measurement = models.ForeignKey(Measurement, on_delete=models.SET_NULL, null=True, verbose_name='Չափման միավոր')
    start_quantity = models.DecimalField(default=1, max_digits=10, decimal_places=2, verbose_name='Սկզբնական չափ')
    wholesale = models.BooleanField(default=False, verbose_name='Մեծածախ')
    min_order_quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Պատվերի մինիմալ չափ', null=True, blank=True)

    class Meta:
        verbose_name = 'Ապրանք'
        verbose_name_plural = 'Ապրանքներ'
        ordering = ['-id']


    def __str__(self):
        return self.title


    @property
    # def ct_model(self):
    #     return self._meta.model_name
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={"slug": self.url})


class Image(models.Model):
    image = models.ImageField(upload_to='photos', verbose_name="Նկար")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', null=True, blank=True,
                                verbose_name="ապրանք")
    gallery = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name = 'Նկար'
        verbose_name_plural = 'Նկարներ'

    def __str__(self):
        return str(self.id)


# class User(AbstractUser):
#     # username = None
#     email = models.EmailField(_('email_address'),unique=True)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']


class Customer(models.Model):
    user = models.OneToOneField(User, verbose_name='Օգտագործող', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Հեռախոսահամար', null=True, blank=True)
    address = models.TextField(verbose_name='Հասցե', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Պատվերներ', related_name='related_order',blank=True )
    # is_email_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Օգտագործող'
        verbose_name_plural = 'Օգտագործողներ'
        ordering = ['-id']


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def get_absolute_url(self):
        return reverse('product', kwargs={"pk": self.id})


class ProductItem(models.Model):
    customer = models.ForeignKey(Customer,blank=True, null=True, on_delete=models.CASCADE, verbose_name="Օգտագործող")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Ապրանք")
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name="Պատվեր", related_name='product_item', null=True, blank=True)
    wholesale = models.BooleanField(default=False, verbose_name='Մեծածախ')
    quantity = models.DecimalField(default=1, verbose_name="Քանակ", max_digits=10, decimal_places=1)
    session_key=models.CharField(max_length=1024, blank=True, null=True)


    def total_price(self):
        if self.product.new_price:
            return self.product.new_price * self.quantity
        else:
            return self.product.price * self.quantity


    def qty(self):
        if self.product.start_quantity=='item':
            self.quantity=int(self.quantity)
        return self.quantity

    def __str__(self):
        return f'{self.product.title} - {self.quantity}{self.product.measurement} - {self.total_price()}dr\n'

    class Meta:
        verbose_name = 'Ընտրված ապրանք'
        verbose_name_plural = 'Ընտրված ապրանքներ'
        ordering = ['-id']


class Basket(models.Model):
    customer = models.OneToOneField(Customer, blank=True, null=True, on_delete=models.CASCADE, related_name='baskets',
                                    verbose_name="Օգտագործող")
    productItems = models.ManyToManyField(ProductItem, related_name='product_item', blank=True,
                                          verbose_name="Զամբյուղի ապրանք")
    delivery_cost = models.PositiveIntegerField(default=0, verbose_name="Առաքման արժեքը")
    session_key=models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        if self.customer:
            return str(self.customer.user.username)
        else:
            return str(self.session_key)

    def finale_price(self):
        finale_price = 0
        for i in self.productItems.all():
            if i.product.new_price:
                finale_price += i.product.new_price * i.quantity
            else:
                finale_price += i.product.price * i.quantity
        return finale_price

    def total_quantity(self):
        total = 0
        for i in self.productItems.all():
            total += 1
        return total

    class Meta:
        verbose_name = 'Զամբյուղ'
        verbose_name_plural = 'Զամբյուղներ'
        ordering = ['-id']


class Time_Shipping(models.Model):
    time_shipping = models.CharField(max_length=100, verbose_name="Առաքման ժամ")

    def __str__(self):
        return self.time_shipping

    class Meta:
        verbose_name = 'Առաքման ժամ'
        verbose_name_plural = 'Առաքման ժամեր'


class Order(models.Model):
    STATUS_CHOICES = (
        ('STATUS_NEW', 'Նոր պատվեր'),
        ('STATUS_READY', 'Պատվերը պատրաստ է'),
        ('STATUS_COMPLETED', 'Պատվերը առաքված է'),
    )

    PAYMENT_TYPE_CHOICES = (
        ('TYPE_PAYMENT_CASH', 'Կանխիկ'),
        ('TYPE_PAYMENT_NON_CASH', 'Անկանխիկ')
    )
    BUYING_TYPE_CHOICES = (
        ('BUYING_TYPE_SELF', 'Հաճախորդը կմոտենա'),
        ('BUYING_TYPE_DELIVERY', 'Արաքում')
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Պատվեր կատարող", related_name='related_orders')
    time_shipping = models.ForeignKey(Time_Shipping, on_delete=models.SET_NULL, null=True, verbose_name="Առաքման ժամ")
    # product_items = models.ManyToManyField(ProductItem, verbose_name="Պատվերի ապրանքներ")
    basket = models.ForeignKey(Basket, verbose_name='Զամբյուղ', on_delete=models.CASCADE,related_name='related_basket_orders', null=True, blank=True)
    finale_price = models.PositiveIntegerField(default=0, verbose_name="Ընդհանուր գումար")
    delivery_cost = models.PositiveIntegerField(default=0, verbose_name="Առաքման արժեք")
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='STATUS_NEW')
    city = models.CharField(max_length=200, null=True, verbose_name="Քաղաք")
    address = models.CharField(max_length=200, null=True, verbose_name="Հասցե")
    phone = models.CharField(max_length=100, verbose_name="Հեռախոսահամար")
    date_shipping = models.DateField(verbose_name="Առաքման օր", null=True)
    payment_type = models.CharField(max_length=100, choices=PAYMENT_TYPE_CHOICES, null=True)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Ավելացվել է", null=True)

    def __str__(self):
        return f'{self.id} {self.customer.user.first_name}'

    class Meta:
        verbose_name = 'Պատվեր'
        verbose_name_plural = 'Պատվերներ'
        ordering = ['date_shipping', 'time_shipping']






