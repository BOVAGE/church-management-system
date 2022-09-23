from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.contrib.auth import logout
from .forms import UserCreationForm, ProfileForm, UserEditForm
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    context = {"user": user, "profile": profile}
    return render(request, "user/profile.html", context)


def edit_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    if request.user != user:
        raise PermissionDenied()
    if request.method != "POST":
        user_form = UserEditForm(instance=user)
        profile_form = ProfileForm(instance=profile)
    else:
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile Update Successfully.")
            return redirect("user:profile", user_id=user.id)
        else:
            messages.error(request, "Error Updating your profile")
    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, "user/profile_edit.html", context)


def register(request):
    if request.method != "POST":
        user_form = UserCreationForm()
        profile_form = ProfileForm()
    else:
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_profile = profile_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password1"])
            new_user.save()
            new_user.profile.bio = profile_form.cleaned_data["bio"]
            new_user.profile.pic = profile_form.cleaned_data["pic"]
            new_user.profile.social_link = profile_form.cleaned_data["social_link"]
            new_user.profile.role = profile_form.cleaned_data["role"]
            new_user.save()
            # new_profile.user = new_user
            # new_profile.save()
            messages.success(request, "Account created Successfully.")
            return redirect("user:login")
        else:
            messages.error(request, "Error  creating your account")
    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, "user/register.html", context)


def log_out(request):
    logout(request)
    messages.success(request, "Logout Successfully.")
    return redirect("blog:index")
