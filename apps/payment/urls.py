from django.urls import path
from .views import transact, verfiy_payment, success, failure

app_name = "payment"
urlpatterns = [
    path("", transact, name="donate"),
    path("verify/<str:reference>/", verfiy_payment, name="verify"),
    path("success/", success, name="sucess"),
    path("failure/", failure, name="failure"),
]
