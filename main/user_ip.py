from .models import Customer


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def save_user_ip_address(request, user):
    profile = Customer.objects.get(user=user)
    profile.ip_address = get_client_ip(request)
    profile.save()
