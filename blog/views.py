from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required, user_passes_test
import markdown

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
    # Busca o post pelo slug
    post = get_object_or_404(Post, slug=slug)

    # Renderiza o conteúdo do post em Markdown usando o filtro `render_markdown`
    post_content_html = markdown.markdown(
        post.content, extensions=["fenced_code", "codehilite"]
    )

    # Passa o post e o conteúdo em HTML para o template
    context = {
        "post": post,
        "post_content_html": post_content_html,
    }

    return render(request, "post_detail.html", context)


def markdown_content_view(request, slug):
    markdown_content = get_object_or_404(Post, slug=slug)
    context = {"markdown_content": markdown_content}
    return render(request, "post_detail.html", context=context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def post_add(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        slug = slugify(title)
        post = Post.objects.create(
            title=title, content=content, slug=slug, author=request.user
        )
        post.tags.set(request.POST.getlist("tags"))  # Associar as tags ao post
        post.save()
        messages.success(request, "Post criado com sucesso!")
        return redirect("post_detail", slug=post.slug)

    # Carregar todas as tags para exibição no formulário
    tags = Tag.objects.all()
    context = {"tags": tags}
    return render(request, "post_add.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.cover = request.POST.get(
            "cover", post.cover
        )  # Adicionando capa, caso seja alterada
        post.save()
        post.tags.set(request.POST.getlist("tags"))  # Atualiza as tags associadas
        messages.success(request, "Post atualizado com sucesso!")
        return redirect("post_detail", slug=post.slug)

    tags = Tag.objects.all()
    context = {"post": post, "tags": tags}
    return render(request, "post_edit.html", context)
