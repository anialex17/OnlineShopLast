from django.urls import path
from .views import *

urlpatterns = [
    path('password/', PasswordsChangeView.as_view(template_name='main/password_change.html')),
    path('password_success/', password_success, name='password_success'),

    path('profile/<int:pk>/', customer, name='profile'),
    path('', HomeView.as_view(), name='home'),

    # path('cart/', CartView.as_view(), name='cart'),
    # path('add-to-cart/<str:slug>/', AddToCart.as_view(), name='add_to_cart'),
    # path('remove-from-cart/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    # path('change-qty/<str:ct_model>/<str:slug>/', ChangeQTYView.as_view(), name='change_qty'),
    # path('checkout/', checkout, name='checkout'),
    path('activate/<uidb64>/<token>/', VerificationView.as_view(), name='activate'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('category/<str:category_slug>', ProductListView.as_view(), name='category_product_list'),
    path('<str:category_slug>/<slug:slug>/', ProductDetailView.as_view(), name='product'),
    path('edit-profile', UserEditView.as_view(), name='edit_profile'),

]


