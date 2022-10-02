from django.contrib import admin
from .models import Donation

# Register your models here.
class DonationAdmin(admin.ModelAdmin):
    list_display = ["full_name", "amount", "email_address", "date", "paid", "ref_id"]
    list_filter = ["full_name", "paid", "date"]


admin.site.register(Donation, DonationAdmin)
