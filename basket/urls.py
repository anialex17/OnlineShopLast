from django.urls import path
from . import views

urlpatterns = [
    path('basket/', views.basket, name="basket"),
    path('add_to_basket/', views.add_to_basket, name='add_to_basket'),
    path('basket_remove/', views.basket_remove, name='basket_remove'),
    # path('sipping/', views.shipping, name='shipping'),
    path('ordering/', views.order, name='ordering'),
    path('change_qty_plus/', views.change_qty_plus, name='change_qty_plus'),
    path('change_qty_minus/', views.change_qty_minus, name='change_qty_minus'),
    path('payment_response/', views.payment_response, name='payment_response'),

]