from django.urls import path
from .views import (
    ProductListView,
    CategoryListView,
    ProductWholeSaleListView,
    ProductDetailView,
    CategoryWholeSaleListView,
    SendMessage,
    RegisterView,
    CustomerView,
    BasketView, OrderView, TimeShippingView, AuthInfoView, MyObtainTokenPairView,LogoutView
)

urlpatterns = [

    path('customer/<int:pk>/', CustomerView.as_view()),
    path('auth-info/', AuthInfoView.as_view(), name='auth-info'),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('category/<str:category_slug>/', ProductListView.as_view()),
    path('wholesale/<str:category_slug>/', ProductWholeSaleListView.as_view()),
    path('<str:category_slug>/<int:pk>/', ProductDetailView.as_view()),
    path('category/', CategoryListView.as_view()),
    path('wholesale/', CategoryWholeSaleListView.as_view()),
    path('send-message/', SendMessage.as_view()),
    path('register/', RegisterView.as_view()),
    path('basket/', BasketView.as_view()),
    path('order/', OrderView.as_view()),
    path('time-shipping/', TimeShippingView.as_view()),
]
