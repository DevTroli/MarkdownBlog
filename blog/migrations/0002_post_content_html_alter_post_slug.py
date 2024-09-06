# Generated by Django 5.1 on 2024-08-21 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="content_html",
            field=models.TextField(blank=True, editable=False),
        ),
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.SlugField(max_length=102, unique=True),
        ),
    ]
