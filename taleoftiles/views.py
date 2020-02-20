from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from .models import Post, Tag, Collection, Setting, Product, Sampler, Sample
from .models import Config, Shipping

from .forms import NewSamplerShipping

import numpy as np
import datetime as dt

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

def about(request):
    return render(request, "about.html",)

def askaquestion(request):
    return render(request, "askaquestion.html",)

def contacts(request):
    return render(request, "contacts.html",)

def termsandcond(request):
    return render(request, "termsandcond.html",)

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
    try: 
        setting = Setting.objects.get(publication__slug  = setting_slug )
    except ObjectDoesNotExist:
        return render(request, "_404.html",{"message":"The setting you asked to review is not existing",})

    return render(request, "setting.html",{"setting":setting })
 

def shipping(request, internal_tracking_id):
    try: 
        #the goo sampler is the one that has not being shipped
        shipping = Shipping.objects.get(internal_tracking_id  = internal_tracking_id,  )
    except ObjectDoesNotExist:
        return render(request, "_404.html",{"message":"The shipping you asked to view is not existing",})   

    return render(request, "shipping.html",{"shipping":shipping,})

def ship_sampler(request, session_id):
    # if we have less than 4 samples in the samples..
    # if there is not an user logged
    conf_num_samples = Config.objects.get(active = True, tag = "num_samples")
    form = NewSamplerShipping()

    try: 
        #the goo sampler is the one that has not being shipped
        sampler = Sampler.objects.get(session_id  = session_id,  )
    except ObjectDoesNotExist:
        return render(request, "_404.html",{"message":"The sampler you asked to ship is not existing",})
    
    sampler.completion_status = 'c'
    sampler.save()

    form.sampler_id = sampler.pk

    if request.method == 'POST':

        form = NewSamplerShipping(request.POST)

        if form.is_valid():
            
            sampler.completion_status = 'o'
            sampler.save()
            
            form.save()
            shipping = Shipping.objects.latest('id')

            return render(request, "shipping.html",{"shipping":shipping,})

    return render(request, "ship_sampler.html",{"sampler":sampler,'form':form,
            'diff_num_samples':( conf_num_samples.int_val - sampler.sample.filter(removed = False).count()) })

def sampler(request, session_id):
    
    try: 
        sampler = Sampler.objects.get(session_id  = session_id )
    except ObjectDoesNotExist:
        # mettere controlli per vedere se session_id potrebbe essere veramente 
        # una sessione valida altrimenti si rischia il ddos
        sampler = Sampler(session_id  = session_id)
        sampler.save()

    if sampler.completion_status == 'o':
        return ship_sampler(request,session_id)

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

    sample.removed = True;
    sample.save()
    return redirect(request.META.get('HTTP_REFERER'))   

#Check if the product is suitable for sampling for 
#check if we do have a connected use
def product(request, product_slug):
    session_id = request.session._get_or_create_session_key()
    product = Product.objects.get(publication__slug  = product_slug )
    message = ""
    sampler = None
    sample = None
    make_it_new = False
    #attributing to this session a permanence in the database
    try: 
        sampler = Sampler.objects.get(session_id  = session_id )
    except ObjectDoesNotExist:
        sampler = Sampler(session_id  = session_id)
        sampler.save()

    try:
        sample = Sample.objects.get(sampler__pk  = sampler.pk, removed = False, product__publication__slug = product_slug )

    except ObjectDoesNotExist:
        message = "Add this to your free sampler for receiving it at home"
        make_it_new = True

    if request.method == 'POST' and make_it_new:
        # distinguis from chart post to the sampler post    
        sample = Sample(sampler = sampler, product = product)
        sample.save()
        message = "Product added to your sampler"

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

