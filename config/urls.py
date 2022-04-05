from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from .yasg import urlpatterns as doc_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # path('', include('social_django.urls', namespace='social')),
    path('auth/', include('rest_framework_social_oauth2.urls')),
    path('admin/', admin.site.urls),
    path('api/api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('rest_framework_social_oauth2.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/', include('api.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include('social_django.urls', namespace='social'))

]
urlpatterns+=doc_urls

urlpatterns += i18n_patterns(
    path('', include('main.urls')),
    path('', include('pages.urls')),
    path('', include('basket.urls')),
    path('', include('payment.urls')),
    # path('', include('social_django.urls', namespace='social')),
    path('password_reset/done/',
         views.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         views.PasswordResetConfirmView.as_view(template_name="main/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'),
         name='password_reset_complete'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
