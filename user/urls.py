from django.urls import path, include
from .views import profile, log_out, register, edit_profile
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordChangeView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordChangeDoneView,
    PasswordResetCompleteView,
)

app_name = "user"
urlpatterns = [
    path("logout/", log_out, name="log_out"),
    path("register/", register, name="register"),
    path("profile/<int:user_id>/", profile, name="profile"),
    path("profile/edit/<int:user_id>/", edit_profile, name="edit"),
    path("profile/<int:id>/", profile, name="profile"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "password_reset/",
        PasswordResetView.as_view(success_url=reverse_lazy("user:password_reset_done")),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("user:password_reset_conplete")
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done",
        PasswordResetCompleteView.as_view(),
        name="password_reset_conplete",
    ),
    path(
        "password_change/",
        PasswordChangeView.as_view(
            success_url=reverse_lazy("user:password_change_done")
        ),
        name="password_change",
    ),
    path(
        "password_change/done",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]
