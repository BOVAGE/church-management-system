from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Repeat Password")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        help_texts = {"username": None}

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if first_name.strip() == "":
            raise forms.ValidationError("First name is required")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if last_name.strip() == "":
            raise forms.ValidationError("Last name is required")
        return last_name

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password1


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        help_texts = {"username": None}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "pic", "role", "social_link"]
