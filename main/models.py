from django.utils import timezone
import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse


# User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=250, verbose_name='Կատեգորիա')
    image = models.ImageField(upload_to='photos', verbose_name="Նկար")
    url = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Կաեգորիա'
        verbose_name_plural = 'Կատեգորիաներ'

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Կատեգորիա', null=True, blank=True)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media', null=True, blank=True)
    url = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    product_type = models.CharField(max_length=255)
    # delivery_time = models.CharField(max_length=10)
    # delivery_cost = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Ապրանք'
        verbose_name_plural = 'Ապրանքներ'

    def __str__(self):
        return self.title

    @property
    def ct_model(self):
        return self._meta.model_name

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


class Customer(models.Model):
    user = models.OneToOneField(User, verbose_name='Օգտագործող', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Հեռախոսահամար', null=True, blank=True)
    address = models.TextField(verbose_name='Հասցե', null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Օգտագործող'
        verbose_name_plural = 'Օգտագործողներ'

    def __str__(self):
        # return f'{self.user.first_name} {self.user.last_name}'
        return f'{self.user.username} '

    def get_absolute_url(self):
        return reverse('product', kwargs={"pk": self.id})


class ProductItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True,verbose_name="Օգտագործող")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name="Ապրանք")
    quantity = models.IntegerField(default=1,verbose_name="Քանակ")

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product.title}---{self.quantity}'

    class Meta:
        verbose_name = 'Ընտրված ապրանք'
        verbose_name_plural = 'Ընտրված ապրանքներ'
        ordering = ['-id']


class Basket(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='baskets', verbose_name="Օգտագործող")
    productItems = models.ManyToManyField(ProductItem, related_name='product_item', blank=True, verbose_name="Զամբյուղի ապրանք")
    delivery_cost = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.customer.user.username)

    def finale_price(self):
        finale_price = 0
        for i in self.productItems.all():
            print(i)
            finale_price += i.product.price * i.quantity+self.delivery_cost
        return finale_price

    def total_quantity(self):
        total = 0
        for i in self.productItems.all():
            total += i.quantity
        return total

    class Meta:
        verbose_name = 'Զամբյուղ'
        verbose_name_plural = 'Զամբյուղներ'
        ordering = ['-id']


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,verbose_name="Պատվեր կատարող")
    product_items = models.ManyToManyField(ProductItem, verbose_name="Պատվերի ապրանքներ")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Ավելացվել է", null=True)
    finale_price = models.PositiveIntegerField(default=0)
    delivery_cost = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.customer.user.first_name)

    class Meta:
        verbose_name = 'Պատվեր'
        verbose_name_plural = 'Պատվերներ'
        ordering = ['date_added']


class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name="Պատվիրատու")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name="Պատվեր")
    city = models.CharField(max_length=200, null=False, verbose_name="Քաղաք")
    address = models.CharField(max_length=200, null=False, verbose_name="Հասցե")
    phone = models.CharField(max_length=100, verbose_name="Հերախոսահամար")
    date_time_shipping = models.DateTimeField(verbose_name="Պատվերի օր և ժամ", null=True)

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = 'Առաքում'
        verbose_name_plural = 'Առաքումներ'
        ordering = ['date_time_shipping']








