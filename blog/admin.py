from django.contrib import admin
from .models import Announcement, Category, Comment, Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_created']
    list_filter = ['title', 'author', 'date_created']
    search_fields = ['title', 'body', 'description']
    prepopulated_fields = {'slug': ('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment_text', 'post']
    search_fields = ['user__username', 'comment_text', 'post__title']
    list_filter = ['user', 'post']

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
admin.site.register(Announcement)