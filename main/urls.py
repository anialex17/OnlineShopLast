from django.urls import path
from .views import *

urlpatterns = [
    path('password/', PasswordsChangeView.as_view(), name='password_change'),
    path('password_success/', password_success, name='password_success'),
    path('profile/<int:pk>/', customer, name='profile'),
    path('', HomeView.as_view(), name='home'),
    path('wholesale', WholeSaleView.as_view(), name='wholesale'),
    path('activate/<uidb64>/<token>/', VerificationView.as_view(), name='activate'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('wholesale/<str:category_slug>', ProductWholeSaleListView.as_view(), name='category_wholesale_product_list'),
    path('category/<str:category_slug>', ProductListView.as_view(), name='category_product_list'),
    # path('category/<str:category_slug>', WholeSaleProductView.as_view(), name='wholesale_product_list'),
    path('<str:category_slug>/<slug:slug>/', ProductDetailView.as_view(), name='product'),
    # path('edit-profile', UserEditView.as_view(), name='edit_profile'),
    path('edit-profile', edit_profile, name='edit_profile'),

]
