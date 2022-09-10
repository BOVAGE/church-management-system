from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from .forms import PaymentForm
from .models import Donation
import requests
import datetime

# Create your views here.
transaction_url = "https://api.paystack.co/transaction/"


@login_required(login_url="user:login")
def transact(request):
    user = request.user
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.date = datetime.datetime.now()
            instance.save()
            print(instance.ref_id)
            return JsonResponse({"ref_id": instance.ref_id})
        else:
            return redirect(reverse("payment:donate"))
    form = PaymentForm(
        initial={
            "full_name": f"{user.first_name} {user.last_name}",
            "email_address": user.email,
        }
    )
    context = {"form": form}
    return render(request, "payment/payment_form.html", context)


def verfiy_payment(request, reference):
    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET}"}
    response = requests.get(f"{transaction_url}verify/{reference}", headers=headers)
    print(response.url)
    data = response.json()
    if data["data"]["status"] == "success":
        instance = Donation.objects.get(ref_id=reference)
        instance.paid = True
        instance.save()
    return JsonResponse(data, safe=False)


def success(request):
    return render(request, "payment/success.html")


def failure(request):
    return render(request, "payment/failure.html")
