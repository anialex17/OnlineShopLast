from django.urls import path
from .views import *
from basket.views import *

urlpatterns = [
    path('success/', success, name='success'),
    path('fail/', fail, name='fail'),

]