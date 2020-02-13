from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from .models import Post, Tag, Collection, Setting, Product, Sampler, Sample

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


#Check if the product is suitable for sampling for 
#check if we do have a connected use
def product(request, product_slug):
    session_id = request.session._get_or_create_session_key()
    product = Product.objects.get(publication__slug  = product_slug )
    message = ""
    sampler = None
    sample = None
    
    #attributing to this session a permanence in the database
    try: 
        sampler = Sampler.objects.get(session_id  = session_id )
    except ObjectDoesNotExist:
        sampler = Sampler(session_id  = session_id)
        sampler.save()

    if request.method == 'POST':
    # distinguis from chart post to the sampler post    
        try:
            sample = Sample.objects.get(sampler__pk  = sampler.pk, product__publication__slug = product_slug )
            message = "You already have this in your sampler"

        except ObjectDoesNotExist:
            sample = Sample(sampler  = sampler, product = product)
            sample.save()
            message = "Product added to your sampler"
    return render(request, "product.html",{"product":product, 
        "session_id" : session_id ,"message": message,"sample" : sample})

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

