from django.contrib import messages
from django.shortcuts import redirect
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.html import escape

from main.models import Category, Product, Customer, Basket, Order, Time_Shipping
from main.email import send_activate_mail
from pages.models import SendMessage


class ProductListSerializer(serializers.ModelSerializer):
    category=serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductDetailSerializer(serializers.ModelSerializer):
    category=serializers.StringRelatedField(read_only=True)
    measurement=serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SendMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendMessage
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone',
            'password',
            'password2',
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Email unique validation
        if User.objects.filter(email=validated_data['email']):
            raise serializers.ValidationError({"email": "This email is already registered. Please try another!"})

        # Get username from email
        username_from_email = validated_data['email'].split('@')[0]
        username = ''.join(e for e in username_from_email if e.isalnum())

        first_name_validated = escape(validated_data['first_name'])
        last_name_validated = escape(validated_data['last_name'])

        # Create User
        user = User.objects.create(
            first_name=first_name_validated,
            last_name=last_name_validated,
            username=username,
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()

        # Create Customer
        customer = Customer.objects.create(
            user=user,
            phone=validated_data['phone']
        )
        # send activate mail
        send_activate_mail(request=self.context['request'], user=user)

        # Initializing additional profile related models
        Basket.objects.create(customer=customer)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }

        user_obj = (
            User.objects.filter(email=attrs.get("username")).first() or
            User.objects.filter(username=attrs.get("username")).first()
        )

        if user_obj:
            credentials['username'] = user_obj.username

        return super().validate(credentials)


class CustomerSerializer(serializers.ModelSerializer):
    orders = serializers.StringRelatedField(many=True,read_only=True)

    class Meta:
        model = Customer
        fields = "__all__"


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class Time_ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time_Shipping
        fields = "__all__"
