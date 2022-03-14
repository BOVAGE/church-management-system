from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from .models import Post, Category, Comment
from .forms import CommentForm, PostForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages


# Create your views here.
def index(request):
    category = request.GET.get('category')
    if category == None:
        all_posts = Post.objects.all()
    else:
        all_posts = Post.objects.filter(category__category_name=category)
    paginator = Paginator(all_posts, 3) # Show 3 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    all_categories = Category.objects.all()
    context = {'all_posts': all_posts, 'all_categories': all_categories, 'page_obj': page_obj}
    return render(request, 'blog/index.html', context)

def about(request):
    return render(request, 'blog/about.html')

def detail(request, title):
    post = get_object_or_404(Post, title=title)
    comments = post.comment_set.all()
    if request.method != 'POST':
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        #if user isn't logged in redirect the user
        #to login page, after successful login 
        #user should be back at the comment page
        #more like using next
        if not request.user.is_authenticated:
            return redirect('/user/login/?next='+ request.path +'#comments')
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            return redirect('blog:detail', title= post.title)
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, 'blog/detail.html', context)

@login_required(login_url='user:login')
def create_post(request):
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request, "Post Created Successfully.")
            return redirect('blog:detail', title=instance.title)
        else:
            messages.error(request, "Error Creating the Post.")
    context = {'form': form}
    return render(request, 'blog/post_new.html', context)

def edit_post(request, title):
    post = get_object_or_404(Post, title=title)
    if request.user != post.author:
        raise PermissionDenied()
    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post Edited Successfully.")
            return redirect('blog:detail', title=post.title)
        else:
            messages.error(request, "Error Editing the Post.")
    context = {'form': form}
    return render(request, 'blog/post_edit.html', context)    

def error_404(request, exception):
    return render(request, 'blog/404.html')

def error_403(request, exception):
    return render(request, 'blog/403_csrf.html')

            