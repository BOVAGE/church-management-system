from datetime import date
from django.contrib import messages
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.text import slugify
from utils.bible_books import BIBLE_CHOICES
import requests

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category_name


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=50, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    post_image = models.ImageField(upload_to="media/")
    body = RichTextField()
    # body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-last_modified"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:detail",
            args=(
                self.id,
                self.slug,
            ),
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment_text


class Announcement(models.Model):
    event_name = models.CharField(max_length=50)
    featured = models.BooleanField()  # only set one announcement to be True
    event_date = models.DateTimeField(blank=True)

    # order the annonument of the events in order of the closet event-date
    # the closet event date comes first
    class Meta:
        ordering = ["event_date"]

    def __str__(self):
        return self.event_name


class TodayBibleVerse(models.Manager):
    def get_queryset(self):
        return super(TodayBibleVerse, self).get_queryset().filter(date_for=date.today())


class BibleVerse(models.Model):
    bible_verse = models.CharField(max_length=20, choices=BIBLE_CHOICES)
    ref = models.CharField(
        max_length=10,
        help_text="Write in this format: \
                            chapter:verse and chapter:start-end in case of range",
    )
    date_for = models.DateField()

    objects = models.Manager()
    today = TodayBibleVerse()

    def __str__(self):
        return f"{self.bible_verse} {self.ref}"

    def get_bible_verse(self):
        verse_ref = str(self)
        url = "https://bible-api.com/" + verse_ref
        print(url)
        response = requests.get(url).json()
        text = response["text"]
        return text
