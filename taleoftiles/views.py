from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .models import Post, Tag, Collection, Setting, Product

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
    collections = Collection.objects.filter()
    settings = Setting.objects.filter()
    
    return render(request, "index.html",{ "collections":collections,"settings" : settings})

def collection(request, collection_slug):
    collection = Collection.objects.get(publication__slug  = collection_slug )
    return render(request, "collection.html",{"collection":collection })

def post(request, post_slug):
    #post = Post.objects.get(slug = post_slug )
    post = Post.objects.get( )
    return render(request, "post.html",{"post":post})

def settings(requests):
    pass

def setting(request, setting_slug):
    pass    

def product(request, product_slug):
    gino = 0
    if request.method == 'POST':
        try:
            gino = int(request.session['fav_color']) + 1
            request.session['fav_color'] = str(gino)
        except KeyError:
            gino = 0
            request.session['fav_color'] = str(0)

    product = Product.objects.get(publication__slug  = product_slug )
    return render(request, "product.html",{"product":product, "gino":gino })

def products(request):
    pass
    
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

