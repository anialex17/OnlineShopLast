from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings


def send_activate_mail(request, user):
    current_site = get_current_site(request)
    email_body = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }

    link = reverse('activate-account', kwargs={
        'uidb64': email_body['uid'],
        'token': email_body['token']
    })

    email_subject = 'Activate your account!'
    activate_url = f'{request.META.get("HTTP_ORIGIN")}{link}'
    email_message = f'Hi {user.username}. ' \
                    f'Follow the link below to activate your account \n ' \
                    f'{activate_url}'

    email = EmailMessage(
        email_subject,
        email_message,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    email.send(fail_silently=False)