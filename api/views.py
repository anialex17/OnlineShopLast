from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import logout

from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import authentication

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from main.models import Product, Category, Customer, Basket, Order, Time_Shipping
from .serializers import (ProductListSerializer,
                          CategoryListSerializer,
                          ProductDetailSerializer,
                          SendMessageSerializer,
                          RegisterSerializer,
                          CustomerSerializer, BasketSerializer, OrderSerializer, Time_ShippingSerializer, CustomTokenObtainPairSerializer)


class APIListPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 20


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = APIListPagination

    def get_queryset(self):
        products = Product.objects.filter(category__url=self.kwargs.get("category_slug"), wholesale=False,
                                          is_published=True)
        return products


class ProductWholeSaleListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = APIListPagination

    def get_queryset(self):
        products = Product.objects.filter(category__url=self.kwargs.get("category_slug"), wholesale=True,
                                          is_published=True)
        return products


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.filter(is_published=True)


class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    pagination_class = APIListPagination

    def get_queryset(self):
        categories = Category.objects.annotate(cnt=Count('product')).filter(product__wholesale=False).filter(cnt__gt=0)
        return categories


class CategoryWholeSaleListView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    pagination_class = APIListPagination

    def get_queryset(self):
        categories = Category.objects.annotate(cnt=Count('product')).filter(product__wholesale=True).filter(cnt__gt=0)
        return categories


class SendMessage(generics.CreateAPIView):
    serializer_class = SendMessageSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class CustomerView(generics.RetrieveAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class BasketView(generics.ListAPIView):
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()


class OrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = OrderSerializer


class TimeShippingView(generics.ListAPIView):
    serializer_class = Time_ShippingSerializer
    queryset = Time_Shipping.objects.all()


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request, *args, **kwargs):
        response = super(MyObtainTokenPairView, self).post(request, *args, **kwargs)

        customer = (
                Customer.objects.filter(user__email=request.data.get('username')).first() or
                Customer.objects.filter(user__username=request.data.get('username')).first()
        )

        user_profile = CustomerSerializer(customer, many=False, context={'request': request}).data

        data = {
            'tokens': response.data,
            'profile_data': {
                'customer': user_profile,
            }
        }
        return Response(data)


class AuthInfoView(APIView):
    def get(self, request):
        data = {'is_authenticated': False}

        if request.user.is_authenticated:
            customer = Customer.objects.filter(user_id=request.user.id).first()
            user_profile = CustomerSerializer(customer, many=False, context={'request': request}).data
            data = {
                'profile_data': {
                    'customer': user_profile,
                }
            }
        return Response(data)


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return Response("You have successfully logged out!")