from django.urls import path
from .views import index

app_name = 'sermon'
urlpatterns = [
    path('', index, name='sermons'),
]