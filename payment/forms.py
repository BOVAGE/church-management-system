from django.forms import ModelForm
from .models import Donation


class PaymentForm(ModelForm):
    class Meta:
        model = Donation
        exclude = ["date", "paid", "ref_id"]
