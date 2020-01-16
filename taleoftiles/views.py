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
    return render(request, "post.html",{"post":post})

def blog(request, tag_slug = None):

    if(tag_slug == None):
        #filter just the ones that have publish date bigger than today
        posts = Post.objects.filter(publish_date__gte= date.today()  )
        menu_tags = Tag.objects.filter(in_menu = True)
    else:
        posts = Post.objects.filter(publish_date__gte= date.today()  )
        menu_tags = Tag.objects.filter(in_menu = True)

    return render(request, "blog.html", {"posts": posts, "menu_tags" : menu_tags})

