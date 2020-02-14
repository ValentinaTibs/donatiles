from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from .models import Post, Tag, Collection, Setting, Product, Sampler, Sample
from .models import Config

import requests
import logging


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



def sampler(request, session_id):
    try: 
        sampler = Sampler.objects.get(session_id  = session_id,  )
    except ObjectDoesNotExist:
        # mettere controlli per vedere se session_id potrebbe essere veramente 
        # una sessione valida altrimenti si rischia il ddos
        sampler = Sampler(session_id  = session_id)
        sampler.save()

    try: 
        conf = Config.objects.get(active = True, tag = "num_samples")
    except ObjectDoesNotExist:
        conf = Config(tag = "num_samples", int_val  = 4)
        conf.save()  

    samples = list(sampler.sample.filter(removed = False))
    samples_len = len(samples)

    for i in range(samples_len,conf.int_val):
        samples = samples + [None]

    return render(request, "sampler.html",{"sampler":sampler,"samples":samples})


def del_sample(request, session_id, product_id):
    try: 
        sample = Sample.objects.get(sampler__session_id  = session_id, product__pk = product_id, )
    except ObjectDoesNotExist:
        # mettere controlli per vedere se session_id potrebbe essere veramente 
        # una sessione valida altrimenti si rischia il ddos
        conf = Config.objects.get(active = True, tag = "message_del_sample")
        return render(request, "_404.html",{"message":conf.char_val})
        
    sampler(request,session_id)

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
            sample = Sample.objects.get(sampler__pk  = sampler.pk,removed = False, product__publication__slug = product_slug )
            message = "You already have this in your sampler"

        except ObjectDoesNotExist:
            sample = Sample(sampler = sampler, product = product)
            sample.save()
            message = "Product added to your sampler"

    print("HERE WE GO WITH THE RENDERING")
    print(product)
    print(session_id)
    return render(request, "product.html",{"product":product, 
            "message": message,"sample" : sample,"sampler" : sampler,
        })

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

