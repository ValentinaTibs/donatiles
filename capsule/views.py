from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render

from capsule.models import Influencer
# Create your views here.

def index(request,_name):  

    try: 
        art_caps = Influencer.objects.get(name__slug  = _name )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message":"The Capsule you are looking for is not existing",}) 

    return render(request, "capsulette.html",{
        "art_caps": art_caps,
        })

