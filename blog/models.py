from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=102, unique=True)
    cover = models.URLField(max_length=200, blank=True, null=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="posts")
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
