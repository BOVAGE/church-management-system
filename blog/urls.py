from django.urls import path
from .views import edit_post, index, detail, about, create_post, delete_post

app_name = 'blog'
urlpatterns = [
    path('', index, name='index'),
    path('post/new/', create_post, name='new'),
    path('post/<str:title>/', detail, name='detail'),
    path('post/<str:title>/delete', delete_post, name='delete'),
    path('post/<str:title>/edit', edit_post, name='edit'),
    path('about/', about, name='about'),
]