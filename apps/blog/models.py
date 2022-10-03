from datetime import date

import requests
from ckeditor.fields import RichTextField
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from apps.utils.bible_books import BIBLE_CHOICES

User = get_user_model()


class Category(models.Model):
    """class for Category DB Table"""

    category_name = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        """Returns string representation of category object"""
        return self.category_name


class Post(models.Model):
    """Class for Post DB Table"""

    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=50, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    post_image = models.ImageField(upload_to="media/")
    body = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-last_modified"]

    def __str__(self) -> str:
        """Returns string representation of post object"""
        return self.title

    def get_absolute_url(self) -> str:
        """Returns the canonical URL (post detail URL) for post object"""
        return reverse(
            "blog:detail",
            args=(
                self.id,
                self.slug,
            ),
        )

    def save(self, *args, **kwargs):
        """Save method includes slugify"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    """Class for Comment DB Table"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Returns string representation of Comment object"""
        return self.comment_text


class Announcement(models.Model):
    """Class for Announcement DB Table"""

    event_name = models.CharField(max_length=50)
    featured = models.BooleanField()  # only set one announcement to be True
    event_date = models.DateTimeField(blank=True)

    # order the announcement of the events in order of the closet event-date
    # the closet event date comes first
    class Meta:
        ordering = ["event_date"]

    def __str__(self) -> str:
        """Returns string representation of Announcement object"""
        return self.event_name


class TodayBibleVerse(models.Manager):
    def get_queryset(self):
        return super(TodayBibleVerse, self).get_queryset().filter(date_for=date.today())


class BibleVerse(models.Model):
    """Class for Bible Verse DB Table"""

    bible_verse = models.CharField(max_length=20, choices=BIBLE_CHOICES)
    ref = models.CharField(
        max_length=10,
        help_text="Write in this format: \
                            chapter:verse and chapter:start-end in case of range",
    )
    date_for = models.DateField()

    objects = models.Manager()
    today = TodayBibleVerse()

    def __str__(self) -> str:
        """Returns string representation of BibleVerse object"""
        return f"{self.bible_verse} {self.ref}"

    def get_bible_verse(self) -> str:
        """Returns the content for the bible_verse reference"""
        verse_ref = str(self)
        url = "https://bible-api.com/" + verse_ref
        response = requests.get(url).json()
        text = response["text"]
        return text
