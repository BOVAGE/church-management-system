from webbrowser import get
from django.db import models
import uuid

# Create your models here.
class Donation(models.Model):
    full_name = models.CharField(max_length=35)
    email_address = models.EmailField()
    amount = models.DecimalField(decimal_places=2, max_digits=7)
    date = models.DateTimeField()
    ref_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} paid {self.amount}"
