from django.shortcuts import render

from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from layout.models      import Element

def support(request):  
    dyn_elements = Element.objects.filter(tag__parent__slug = 'support', public = True)
    return render(request, "support.html",{
        'layout_elems'  : dyn_elements,
        })

# Create your views here.
