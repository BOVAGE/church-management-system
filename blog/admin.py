from django.contrib import admin
from .models import Announcement, Category, Comment, Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_created']
    list_filter = ['title', 'author', 'date_created']
    search_fields = ['title', 'body', 'description']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Announcement)