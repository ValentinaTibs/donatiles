from django.shortcuts import render
from django.http import HttpResponse
from datetime import date

from .models import Post, Tag

import requests

def index():
    return 

def index(request):
    return render(request, "index.html")

def post(request, post_slug):
    post = Post.objects.get(slug= post_slug )
    return render(request, "blog.html", {"posts": posts, "menu_tags" : menu_tags})

def tag(request, tag_slug):
    posts = Post.objects.filter(publish_date__lte= date.today(), post_tag = tag_slug )
    menu_tags = Tag.objects.filter(in_menu = True)
    return render(request, "blog.html", {"posts": posts, "menu_tags" : menu_tags})

def blog(request):
    posts = Post.objects.filter(publish_date__lte= date.today()  )
    menu_tags = Tag.objects.filter(in_menu = True)

    return render(request, "blog.html", {"posts": posts, "menu_tags" : menu_tags})

