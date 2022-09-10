from django.conf import settings


def get_payment_secret(request):
    context = {"public_key": settings.PAYSTACK_PUBLIC}
    return context
