from django.urls import path
from .views import index, detail, sermon_pdf

app_name = "sermon"
urlpatterns = [
    path("", index, name="sermons"),
    path("<int:year>/<int:month>/<int:day>/<slug:slug>/", detail, name="sermon_single"),
    path("<int:id>/pdf", sermon_pdf, name="sermon_pdf"),
]
