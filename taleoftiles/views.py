from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from taleoftiles.models import Tag, Product, Catalogue
from layout.models      import Element
from blog.models        import Post

from CRM.forms          import NewChartItemForm

def index(request):  
    home_elems = Element.objects.filter(tag__parent__slug = 'home', public = True)
    home_tags = Tag.objects.filter(in_home = True, public = True)
    home_post = Post.active.filter(tags__slug='in-home')
    return render(request, "home.html",{
        'layout_elems'  : home_elems,
        'tags'          : home_tags,
        'posts'         : home_post,
        })

def custom_merge(unit1, unit2):
   # Merge dictionaries and concat values of same keys if list
   out = {**unit1, **unit2}
   for key, value in out.items():
       if key in unit1 and key in unit2 :
               out[key] = value + unit1[key]
   return out

def catalogue(request, the_filter = None):

    catalogue_prod = Product.active.filter(available = True)
    query_dict = {}
    try: 
        cat = Catalogue.objects.get(active = True)
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message":"There is no active catalogue",})

    if the_filter:
        try: 
            tag = Tag.objects.get(slug = the_filter)
        except ObjectDoesNotExist:
            return render(request, "404.html",{"message":"There is no active catalogue",})        
        
        query_dict = custom_merge(query_dict, {tag.parent.slug:[the_filter]})

    if request.method == 'POST':
        query_dict = custom_merge(query_dict,(dict(request.POST.lists()))) 

    catalogue_tags = cat.tags()
    catalogue_prod = cat.filter_products(catalogue_prod,query_dict)

    return render(request, "catalogue.html",{   
        "tags"          : catalogue_tags,  
        "products"      : catalogue_prod,
        "active_tags"   : query_dict
        })

from django.core.mail import send_mail

def product(request, product_code, chi_form = None ):    
    
    try: 
        product = Product.active.get(code = product_code )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message":"The product you asked to view is not existing",}) 

    send_mail('Subject here', 'Here is the message.', 'info@taleoftiles.it', ['tibaldo.valentina@gmail.com'], fail_silently=False)

    #for all product in the same series that are not support and not itself
    related_series  = Product.active.filter(tags = product.get_tag('serie'),support_to = None).exclude(pk = product.pk)
    
    chi_form = NewChartItemForm(request.POST or {'product':product.pk,} , request.FILES or None)

    return render(request, "product.html",{
        "product":product,
        "products_series":related_series,
        "chi_form" : chi_form
        })
