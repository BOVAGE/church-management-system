from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from datetime import date

# Create your models here.
class TodayManager(models.Manager):
    def get_queryset(self):
        return (
            super(TodayManager, self).get_queryset().filter(date_created=date.today())
        )


class Sermon(models.Model):
    """Class for Sermon DB Table"""

    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, related_name="sermons", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/")
    summary = models.CharField(max_length=150)
    content = RichTextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    date_created = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=50)
    tags = TaggableManager()

    # managers
    objects = models.Manager()
    today = TodayManager()

    class Meta:
        ordering = ["-date_created"]
        unique_together = ["slug", "date_created"]

    def __str__(self) -> str:
        """Returns string representation for sermon object"""
        return self.title

    def get_absolute_url(self) -> str:
        """Returns canonical URL (sermon detail URL) for sermon object"""
        return reverse(
            "sermon:sermon_single",
            args=(
                self.date_created.year,
                self.date_created.month,
                self.date_created.day,
                self.slug,
            ),
        )
