import redis
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.urls import reverse

from apps.blog.tasks import today_bible_verse

from apps.blog.forms import CommentForm, PostForm
from apps.blog.models import BibleVerse, Category, Comment, Post
from apps.blog.newsletter import newsletter

# connect to redis
r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


def index(request):
    category = request.GET.get("category", "")
    if not category:
        all_posts = Post.objects.all()
    else:
        all_posts = Post.objects.filter(category__category_name=category)
    paginator = Paginator(all_posts, 3)  # Show 3 posts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    all_categories = Category.objects.all()

    # today's bible verse
    today_bible_verse_obj = BibleVerse.today.first()
    text = "Not loaded Yet"
    if r.get("today_bible_verse") is None:
        today_bible_verse.delay(today_bible_verse_obj.id)
    else:
        text = r.get("today_bible_verse").decode("utf-8")
    bv = {"bible_ref": str(today_bible_verse_obj), "text": text}
    context = {
        "all_posts": all_posts,
        "all_categories": all_categories,
        "page_obj": page_obj,
        "category": category,
        "bv": bv,
    }
    return render(request, "blog/index.html", context)


def about(request):
    return render(request, "blog/about.html")


def detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    comments = post.comment_set.all()
    if request.method != "POST":
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        # if user isn't logged in redirect the user
        # to login page, after successful login
        # user should be back at the comment page
        # more like using next
        if not request.user.is_authenticated:
            return redirect("/user/login/?next=" + request.path + "#comments")
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            return HttpResponseRedirect(
                reverse("blog:detail", args=(post.id, post.slug))
            )
    context = {"post": post, "form": form, "comments": comments}
    return render(request, "blog/detail.html", context)


@login_required(login_url="user:login")
def create_post(request):
    if request.method != "POST":
        form = PostForm()
    else:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request, "Post Created Successfully.")
            return HttpResponseRedirect(
                reverse("blog:detail", args=(instance.id, instance.slug))
            )
        else:
            messages.error(request, "Error Creating the Post.")
    context = {"form": form}
    return render(request, "blog/post_new.html", context)


def edit_post(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    if request.user != post.author:
        raise PermissionDenied()
    if request.method != "POST":
        form = PostForm(instance=post)
    else:
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post Edited Successfully.")
            return HttpResponseRedirect(
                reverse("blog:detail", args=(post.id, post.slug))
            )
        else:
            messages.error(request, "Error Editing the Post.")
    context = {"form": form}
    return render(request, "blog/post_edit.html", context)


def delete_post(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    if request.user != post.author:
        raise PermissionDenied()
    post.delete()
    messages.success(request, f"Post: {post.title} deleted successfully")
    return HttpResponseRedirect(reverse("blog:index"))


def subscribe(request):
    if request.method == "POST":
        email = request.POST["Nemail"]
        response = newsletter.add_member(email_address=email, status="subscribed")
        if response == "added" or response == "updated":
            messages.success(request, "You have been added to our Newsletter plan.")
        elif response == "Member Exists":
            messages.error(request, f"{email} already exists in our newsletter")
        else:
            messages.error(request, "An error occured!")
        return HttpResponseRedirect(reverse("blog:index"))


def unsubscribe(request, email_hash):
    response = newsletter.unsubscribe(email_hash)
    if response == "updated":
        return HttpResponse("You have been unsubscribed from our newsletter!")
    return JsonResponse(response, safe=False)


def error_404(request, exception):
    return render(request, "blog/404.html")


def error_403(request, exception):
    return render(request, "blog/403_csrf.html")
