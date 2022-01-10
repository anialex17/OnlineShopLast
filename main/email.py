from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.conf import settings


def send_activate_mail(request, user):
    user.is_active = False
    user.save()

    current_site = get_current_site(request)
    email_body = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }

    link = reverse('activate', kwargs={
        'uidb64': email_body['uid'],
        'token': email_body['token']
    })

    site_protocol = 'http'
    if request.is_secure():
        site_protocol = 'https'

    email_subject = 'Активируйте вашу учетную запись!'
    activate_url = f'{site_protocol}://{current_site.domain}{link}'
    email_message = f'Привет, {user.username}, ' \
                    f'Перейдите по ссылке ниже, чтобы активировать свой аккаунт \n ' \
                    f'{activate_url}'

    email = EmailMessage(
        email_subject,
        email_message,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    email.send(fail_silently=False)
