from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from taleoftiles.models import Tag, Product, Catalogue
from layout.models      import Element
from blog.models        import Post

def index(request):  
    home_elems = Element.objects.filter(tag__parent__slug = 'home', public = True)
    home_tags = Tag.objects.filter(in_home = True, public = True)
    home_post = Post.active.filter(tags__slug='in-home')
    return render(request, "home.html",{
        'layout_elems'  : home_elems,
        'tags'          : home_tags,
        'posts'         : home_post,
        })

def catalogue(request, the_filter = None):

    catalogue_prod = Product.active.filter(available = True)

    try: 
        cat = Catalogue.objects.get(active = True)
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message":"There is no active catalogue",})

    catalogue_tags = cat.tags()

    if request.method == 'POST':
        catalogue_prod = cat.filter_products(catalogue_prod,request.POST.items())
    
    return render(request, "catalogue.html",{   
        "tags"      : catalogue_tags,  
        "products"  : catalogue_prod
        })

def product(request, product_slug):    

    try: 
        product = Product.active.get(publication__slug = product_slug )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message":"The product you asked to view is not existing",}) 
    
    #for all product in the same series that are not support and not itself
    rel_series  = Product.active.filter(tags = product.serie(),support_to = None).exclude(pk = product.pk)

    return render(request, "product.html",{
        "product":product,
        "products_series":rel_series,
        })



