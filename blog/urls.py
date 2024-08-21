from django.urls import path
from . import views as v

urlpatterns = [
    path("", v.index, name="index"),  # Main index page
    path("post/<slug:slug>/", v.post_detail, name="post_detail"),  # Post detail page
]
