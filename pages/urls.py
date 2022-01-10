from django.urls import path
from .views import *


urlpatterns = [
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('send_sessage', message, name='send_messages'),
    path('terms_order/', TermsOrderView.as_view(), name='terms_order'),
    path('contact/', ContactView.as_view(), name='contact'),
]