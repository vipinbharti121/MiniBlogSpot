from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import PostForm, CommentForm, UserForm
from .models import Post, Comment

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def new_post(request):
    if not request.user.is_authenticated():
        return render(request, 'posts/login.html')
    else:
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.post_logo = request.FILES['post_logo']
            file_type = post.post_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'post': post,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'posts/newpost.html', context)
            post.save()
            return render(request, 'posts/detail.html', {'post': post})
        context = {
            "form": form,
        }
        return render(request, 'posts/newpost.html', context)


def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    post = Post.objects.filter(user=request.user)
    return render(request, 'posts/index.html', {'post': post})


def detail(request, post_id):
    if not request.user.is_authenticated():
        return render(request, 'posts/login.html')
    else:
        user = request.user
        post = get_object_or_404(Post, pk=post_id)
        return render(request, 'posts/detail.html', {'post': post, 'user': user})


def index(request):
    if not request.user.is_authenticated():
        # return render(request, 'posts/login.html')
        posts = Post.objects.all()
        query = request.GET.get("q")
        if query:
            posts = posts.filter(
                Q(post_title__icontains=query) |
                Q(post_author__icontains=query)|
                Q(post_catagory__icontains=query)
            ).distinct()
            return render(request, 'posts/index.html', {'posts': posts})
        return render(request, 'posts/index.html', {'posts': posts})

    else:
        posts = Post.objects.filter(user=request.user)
        query = request.GET.get("q")
        if query:
            posts = posts.filter(
                Q(post_title__icontains=query) |
                Q(post_author__icontains=query)
            ).distinct()
            return render(request, 'posts/index.html', {'posts': posts})
        else:
            return render(request, 'posts/index.html', {'posts': posts})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'posts/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                posts = Post.objects.filter(user=request.user)
                return render(request, 'posts/index.html', {'posts': posts})
            else:
                return render(request, 'posts/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'posts/login.html', {'error_message': 'Invalid login'})
    return render(request, 'posts/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                posts = Post.objects.filter(user=request.user)
                return render(request, 'posts/index.html', {'posts': posts})
    context = {
        "form": form,
    }
    return render(request, 'posts/register.html', context)


def comment(request):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        cm = form.save(commit=False)
        cm.save()
        posts = Post.objects.filter(user=request.user)
        return render(request, 'posts/index.html', {'posts': posts})

