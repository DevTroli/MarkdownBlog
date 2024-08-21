from django.contrib import admin
from .models import Post, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "author")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
