from django.urls import path
from .views import (
    edit_post,
    index,
    detail,
    about,
    create_post,
    delete_post,
    subscribe,
    unsubscribe,
)

app_name = "blog"
urlpatterns = [
    path("", index, name="index"),
    path("post/new/", create_post, name="new"),
    path("post/<int:id>/<slug:slug>/", detail, name="detail"),
    path("post/<int:id>/<slug:slug>/delete", delete_post, name="delete"),
    path("post/<int:id>/<slug:slug>/edit", edit_post, name="edit"),
    path("subscribe", subscribe, name="subscribe"),
    path("unsubscribe/<str:email_hash>", unsubscribe, name="unsubscribe"),
    path("about/", about, name="about"),
]
