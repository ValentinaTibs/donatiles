from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist


from datetime import date
import datetime as dt
import numpy as np

from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

import requests
import logging


# from .models import Post, Tag, Collection, Setting, Product, Sampler, Sample
# from .models import Config, Shipping, ChartItem, Chart

# from .forms import NewSamplerShipping, NewChartItemForm,QuestionForm

from django.db.models import Count

def index(request):
    # collections = Collection.objects.filter(publication__publish_date__lte= dt.date.today())
    # settings = Setting.objects.filter(publication__publish_date__lte= dt.date.today())
    # products = Product.objects.filter(publication__publish_date__lte= dt.date.today())

    # blog_tags = Tag.objects.filter(publication__post_id__isnull = False, in_menu = True).distinct()
    # setting_tags = Tag.objects.filter(publication__setting_id__isnull = False, in_menu = True).distinct()

    # collections = pagination(request,collections,3)
    # settings = pagination(request,settings,3)
    # products = pagination(request,products,3)
    cannolo = ugettext("Sign Up")
    cannolo2 = _("POCCOZIO")

    return render(request, "empty.html",{ "msg" : cannolo,"msg2" : cannolo2})




# def pagination(request, list, num):
#     page = request.GET.get('page')
#     paginator = Paginator(list, num)
#     try:
#         contacts = paginator.page(page)
#     except PageNotAnInteger:
#         contacts = paginator.page(1)
#     except EmptyPage:
#         contacts = paginator.page(paginator.num_pages)
#     return contacts

# def about(request):
#     return render(request, "about.html",)

# def askaquestion(request):
#     return render(request, "askaquestion.html",)

# def contacts(request):

#     form = QuestionForm(request.POST or None, request.FILES or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             return HttpResponseRedirect('/thanks/')

#     return render(request, "contacts.html",{'form': form})

# def termsandcond(request):
#     return render(request, "termsandcond.html",)

# def index(request):
#     collections = Collection.objects.filter(publication__publish_date__lte= dt.date.today())
#     settings = Setting.objects.filter(publication__publish_date__lte= dt.date.today())
#     products = Product.objects.filter(publication__publish_date__lte= dt.date.today())

#     blog_tags = Tag.objects.filter(publication__post_id__isnull = False, in_menu = True).distinct()
#     setting_tags = Tag.objects.filter(publication__setting_id__isnull = False, in_menu = True).distinct()

#     # collections = pagination(request,collections,3)
#     # settings = pagination(request,settings,3)
#     # products = pagination(request,products,3)

#     return render(request, "index.html",{ 
#         "collections":collections,"settings" : settings, "products" : products
#         })


# def collections(request, tag_slug = None):
#     if(tag_slug):
#         collections = Collection.objects.filter(publication__publish_date__lte= dt.date.today(), publication__tag__slug = tag_slug)
#     else:
#         collections = Collection.objects.filter(publication__publish_date__lte= dt.date.today())
#     collections = pagination(request,collections,3)
#     return render(request, "collections.html",{ "collections":collections })

# def collection(request, collection_slug):
#     collection = Collection.objects.get(publication__slug  = collection_slug )
#     return render(request, "collection.html",{"collection":collection })

# def post(request, post_slug):
#     post = Post.objects.get(slug = post_slug )
#     return render(request, "post.html",{"post":post})

# def settings(request, tag_slug = None):
#     if(tag_slug):
#         settings = Setting.objects.filter(publication__publish_date__lte= dt.date.today(), publication__tag__slug = tag_slug )
#     else:
#         settings = Setting.objects.filter(publication__publish_date__lte= dt.date.today())

#     settings = pagination(request,settings,10)
#     return render(request, "settings.html",{ "settings":settings })

# # form = myForm(request.POST or None, request.FILES or None)
# # if request.method == 'POST':
# #     if form.is_valid():
# #         return HttpResponseRedirect('/thanks/')
# # return render_to_response('my_template.html', {'form': form})

# def setting(request, setting_slug):    
#     try: 
#         setting = Setting.objects.get(publication__slug  = setting_slug )
#     except ObjectDoesNotExist:
#         return render(request, "404.html",{"message":"The setting you asked to review is not existing",})

#     return render(request, "setting.html",{"setting":setting })

# def shipping(request, internal_tracking_id = None):

#     if request.method == 'GET':
#         internal_tracking_id = request.GET['tracking_id']
#     try: 
#         #the goo sampler is the one that has not being shipped
#         shipping = Shipping.objects.get(internal_tracking_id  = internal_tracking_id,  )

#     except ObjectDoesNotExist:
#         return render(request, "404.html",{"message":"The shipping you asked to view is not existing",})   

#     return render(request, "shipping.html",{"shipping":shipping,})

# def ship_sampler(request):
#     session_id = request.session._get_or_create_session_key()
    
#     try: 
#         sampler = Sampler.objects.get(session_id  = session_id )

#     except ObjectDoesNotExist:
#         return render(request, "404.html",{"message":"The shipping you asked to view is not existing",})   

#     form = NewSamplerShipping(request.POST or None, request.FILES or None)

#     if request.method == 'POST':

#         # inserire controlli sul fatto che non ci siano altri ordini da questo utente
#         # che ancora non si siano conclusi con un acquisto
#         if form.is_valid():
#             sampler.completion_status = 'o'
#             sampler.save()

#             form.save()
#             shipping = Shipping.objects.latest('id')
#             shipping.sampler = sampler
#             shipping.save()

#             return render(request, "shipping.html",{"shipping":shipping,})

#     return redirect(request.META.get('HTTP_REFERER'))   

# def ship_chart(request):
#     pass

# def chart(request):

#     session_id = request.session._get_or_create_session_key()
    
#     try: 
#         chart = Chart.objects.get(session_id  = session_id )

#     except ObjectDoesNotExist:
#         chart = Chart(session_id  = session_id)
#         chart.save()

#     return render(request, "chart.html",{"chart":chart,})

# def sampler(request):
#     session_id = request.session._get_or_create_session_key()
    
#     try: 
#         sampler = Sampler.objects.get(session_id  = session_id )

#     except ObjectDoesNotExist:
#         sampler = Sampler(session_id  = session_id)
#         sampler.save()

#     form = NewSamplerShipping(request.POST or None, request.FILES or None)

#     try: 
#         conf = Config.objects.get(active = True, tag = "num_samples")
#     except ObjectDoesNotExist:
#         conf = Config(tag = "num_samples", int_val  = 4)
#         conf.save()  

#     samples = list(sampler.sample.filter(removed = False))
#     samples_len = len(samples)

#     for i in range(samples_len,conf.int_val):
#         samples = samples + [None]
    
#     return render(request, "sampler.html",{"sampler":sampler,"samples":samples,'form':form,
#             'diff_num_samples':( conf.int_val - sampler.sample.filter(removed = False).count())})


# def del_sample(request,  product_id):
#     session_id = request.session._get_or_create_session_key()
#     try: 
#         sample = Sample.objects.get(sampler__session_id  = session_id, product__pk = product_id, )
#     except ObjectDoesNotExist:
#         # mettere controlli per vedere se session_id potrebbe essere veramente 
#         # una sessione valida altrimenti si rischia il ddos
#         conf = Config.objects.get(active = True, tag = "message_del_sample")
#         return render(request, "404.html",{"message":conf.char_val})

#     sample.removed = True;
#     sample.save()
#     return redirect(request.META.get('HTTP_REFERER'))   

# def add_product_chart(request, product_slug):

#     session_id = request.session._get_or_create_session_key()
    
#     try: 
#         product = Product.objects.get(publication__slug  = product_slug )
#     except ObjectDoesNotExist:
#         return render(request, "404.html",{"message":"The product you asked to view is not existing",}) 

#     try: 
#         chart = Chart.objects.get(session_id  = session_id )
#     except ObjectDoesNotExist:
#         # mettere controlli per vedere se session_id potrebbe essere veramente 
#         # una sessione valida altrimenti si rischia il ddos
#         chart = Chart(session_id  = session_id)
#         chart.save()

#     # chartitem = ChartItem(chart = chart, product = product)
#     # chartitem.save()
#     if request.method == 'POST':

#         form = NewChartItemForm(request.POST)
        
#         if form.is_valid():
#             chart.completion_status = 'o'
#             chart.save()
            
#             form.save()

#     message = "Product added to your chart"
    
#     return redirect(request.META.get('HTTP_REFERER'))  

# #Check if the product is suitable for sampling for 
# #check if we do have a connected use
# def product(request, product_slug):
#     session_id = request.session._get_or_create_session_key()
    
#     try: 
#         product = Product.objects.get(publication__slug  = product_slug )
#     except ObjectDoesNotExist:
#         return render(request, "404.html",{"message":"The product you asked to view is not existing",}) 

#     message = ""
#     sampler = None
#     sample = None
#     make_it_new = False

#     dt64 = np.datetime64(np.busday_offset(dt.date.today(), product.wait_time, roll='backward'))
#     wait_day = dt.datetime.utcfromtimestamp(dt64.astype(int))#, timezone.utc)
   
#     new_ic_form = NewChartItemForm(product_id = product.pk)

#     #attributing to this session a permanence in the database
#     try: 
#         sampler = Sampler.objects.get(session_id  = session_id )
#     except ObjectDoesNotExist:
#         sampler = Sampler(session_id  = session_id)
#         sampler.save()

#     try:
#         sample = Sample.objects.get(sampler__pk  = sampler.pk, removed = False, product__publication__slug = product_slug )
#         message = "Product added to your sampler"
#     except ObjectDoesNotExist:
#         message = "Add this to your free sampler for receiving it at home"
#         make_it_new = True

#     if request.method == 'POST' and make_it_new:
#         # distinguis from chart post to the sampler post    
#         sample = Sample(sampler = sampler, product = product)
#         sample.save()
#         message = "Product added to your sampler"


#     return render(request, "product.html",{"product":product, 
#             "message": message,"sample" : sample,"sampler" : sampler,
#             "wait_day_64" : dt64, "new_ic_form" : new_ic_form
#         })

# def products(request,tag_slug = None):
#     if(tag_slug):
#         products = Product.objects.filter(publication__publish_date__lte= dt.date.today(), publication__tag__slug = tag_slug )
#     else:
#         products = Product.objects.filter(publication__publish_date__lte= dt.date.today())
    
#     return render(request, "products.html", {"products": products,})

    
# def post(request, tag_slug):
#     #posts = Post.objects.filter(publish_date__lte= date.today(), publication__tag__slug = tag_slug )
#     posts = Post.objects.filter()
#     posts = pagination(request, posts)
#     menu_tags = Tag.objects.filter(in_menu = True)
#     return render(request, "blog.html", {"posts": posts, "menu_tags" : menu_tags})

# def blog(request,tag_slug = None):
    
#     blog_tags = Tag.objects.filter(publication__post_id__isnull = False, in_menu = True).distinct()

#     if(tag_slug):
#         posts = Post.objects.filter(publication__publish_date__lte= dt.date.today(), publication__tag__slug = tag_slug )
#     else:
#         posts = Post.objects.filter(publication__publish_date__lte= dt.date.today()  )
    

#     return render(request, "blog.html", {"posts": posts, "blog_tags" : blog_tags})

