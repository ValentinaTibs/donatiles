from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from capsule.models import Influencer
from taleoftiles.models import Product
# Create your views here.

def index(request,_name):  

    try: 
        art_caps = Influencer.objects.get(name__slug  = _name )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message":"The Capsule you are looking for is not existing",}) 

    return render(request, "capsulette.html",{
        "art_caps": art_caps,
        })


@login_required
def report(request,_name = None):

    if not _name and not request.user.is_staff:
        return render(request, "404.html",{"message":"Unauthorized access to this page to Non staff members.",}) 

    if not _name and request.user.groups.filter(name='Capsule').exists():
        _name = request.user.username
    
    try: 
        art_caps = Influencer.objects.get(name__slug  = _name )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message":"The Capsule you are looking for is not existing",}) 

    return render(request, "report.html",{
        "art_caps": art_caps,
        })

def capsule_product(request, _name, product_code, chi_form = None ):    
    
    try: 
        product = Product.active.get(code = product_code )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message":"The product you asked to view is not existing",}) 

    art_caps = Influencer.objects.get(name__slug  = _name )

    return render(request, "product_capsule.html",{
        "product":product,
        "influencer":art_caps,
        })