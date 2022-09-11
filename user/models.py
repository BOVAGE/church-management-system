from django.conf import settings
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=30, blank=True)
    pic = models.ImageField(blank=True, default="media/avatar.png", upload_to="media/")
    social_link = models.URLField()

    def __str__(self) -> str:
        return self.user.username

    def get_absolute_url(self):
        return reverse("user:profile", args=(self.id,))
