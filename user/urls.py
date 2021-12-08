from django.urls import path, include
from .views import profile, log_out, register, edit_profile

app_name = 'user'
urlpatterns = [
    path('logout/', log_out, name='log_out'),
    path('register/', register, name='register'),
    path('profile/<int:user_id>/', profile, name='profile'),
    path('profile/edit/<int:user_id>/', edit_profile, name='edit'),
    path('profile/<int:id>/', profile, name='profile'),
    path('', include('django.contrib.auth.urls')),
]