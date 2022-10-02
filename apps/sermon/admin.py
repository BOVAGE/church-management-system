from django.contrib import admin
from .models import Sermon

# Register your models here.
class SermonAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "summary", "date_created"]
    list_filter = ["title", "author", "tags"]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Sermon, SermonAdmin)
