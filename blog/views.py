from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import Post, Tag


def index(request):
    query = request.GET.get("q", "")
    tag_slug = request.GET.get("tag")

    # Logs para depuração
    print(f"Query: {query}")
    print(f"Selected Tag: {tag_slug}")

    tags = Tag.objects.all()
    posts = Post.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()

    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug).distinct()

    posts = posts.order_by("-date")

    context = {
        "posts": posts,
        "tags": tags,
        "selected_tag": tag_slug,
    }

    return render(request, "index.html", context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "post_detail.html", {"post": post})
