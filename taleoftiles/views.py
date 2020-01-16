from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .models import Post, Tag

import requests

def pagination(request, list):
    page = request.GET.get('page')
    paginator = Paginator(list, 10)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return contacts

def index():
    return 

def index(request):
    return render(request, "index.html")

def post(request, post_slug):
    #post = Post.objects.get(slug = post_slug )
    post = Post.objects.get( )
    return render(request, "post.html",{"post":post})

def tag(request, tag_slug):
    #posts = Post.objects.filter(publish_date__lte= date.today(), post_tag = tag_slug )
    posts = Post.objects.filter()
    posts = pagination(request, posts)
    menu_tags = Tag.objects.filter(in_menu = True)
    return render(request, "blog.html", {"posts": posts, "menu_tags" : menu_tags})

def blog(request):
    posts = Post.objects.filter(publish_date__lte= date.today()  )
    menu_tags = Tag.objects.filter(in_menu = True)

    return render(request, "blog.html", {"posts": posts, "menu_tags" : menu_tags})

