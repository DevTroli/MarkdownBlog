from django.urls import path
from . import views as v

urlpatterns = [
    path("", v.index, name="index"),  # Main index page
    path("post/<slug:slug>/", v.post_detail, name="post_detail"),  # Post detail page
    path("add/", v.post_add, name="post_add"),  # Criar novo post
    path("post/<slug:slug>/edit/", v.post_edit, name="post_edit"),  # Editar post
]
