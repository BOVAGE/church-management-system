from django import forms
from .models import Category, Post, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_text"]
        widgets = {
            "comment_text": forms.Textarea(
                attrs={"placeholder": "Write your comment here.."}
            ),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "slug", "category", "post_image", "body", "description"]
