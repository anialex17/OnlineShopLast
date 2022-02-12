from django.urls import path
from .views import *


urlpatterns = [
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('send_message', message, name='send_messages'),
    path('terms_order/', TermsOrderView.as_view(), name='terms_order'),
    path('contact/', ContactView.as_view(), name='contact'),
    # path('about-us/', about_us, name='about_us'),
    path('about-us/', AboutUs.as_view(), name='about_us'),
    path('privacy/', Privacy.as_view(), name='privacy'),
]