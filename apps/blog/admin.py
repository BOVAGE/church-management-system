from django.contrib import admin
from apps.blog.models import Announcement, Category, Comment, Post, BibleVerse

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "date_created"]
    list_filter = ["title", "author", "date_created"]
    search_fields = ["title", "body", "description"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CommentInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "comment_text", "post"]
    search_fields = ["user__username", "comment_text", "post__title"]
    list_filter = ["user", "post"]


class BibleVerseAdmin(admin.ModelAdmin):
    list_display = ["bible_verse", "ref", "date_for"]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
admin.site.register(Announcement)
admin.site.register(BibleVerse, BibleVerseAdmin)
