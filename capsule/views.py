from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q 

import json
import math

from capsule.models     import Influencer
from taleoftiles.models import Product,Tag
from CRM.models         import Chart, ChartItem

def index(request,_name):  

    try: 
        influencer = Influencer.objects.get(name__slug  = _name )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message":"The Capsule you are looking for is not existing",}) 

    return render(request, "capsulette.html",{
        "influencer": influencer,
        })


@login_required
def report(request,_name = None):

    if not _name and not request.user.is_staff:
        return render(request, "404.html",{"message":"Unauthorized access to this page to Non staff members.",}) 

    if not _name and request.user.groups.filter(name='Capsule').exists():
        _name = request.user.username
    
    try: 
        influencer = Influencer.objects.get(name__slug  = _name )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message":"The Capsule you are looking for is not existing",}) 
    

    active_tags = Tag.objects.filter(tag_query,public=True) 
    if tag_len > 0 :      
        products_list = Product.objects.filter(is_active = True, tags__in = active_tags).annotate(num_tags=Count('tags')).filter(num_tags=tag_len).distinct().order_by(order_by)
    res = ChartItem.objects.filter(product__tags = influencer)

    return render(request, "report.html",{
        "influencer": influencer,
        })



def add_chart_capsule(request):

    if request.user.is_authenticated:
        query = Q(user = request.user) 
    else:
        if not request.session.exists(request.session.session_key):
            request.session.create()     

        query = Q(session_id  = request.session.session_key) 

    charts = Chart.objects.filter( query , completion_status = 's')
    if charts.count() <= 0:
        chart = Chart(session_id  = request.session.session_key)
        if request.user.is_authenticated:
            chart.user = request.user
        chart.save()
    else:
        chart = charts.first()
        
    # create new chart item with the values retrived
    p = Product.objects.get(pk=request.POST.get('product', None))
    f = int(request.POST.get('finish', None))
    c = request.POST.get('cut', None)
    if( f == 0) :
        f = Tag.objects.get(slug='s_vinylraw')
    elif (f == 3) :
        f = Tag.objects.get(slug='s_fiberglasss')
    
    q = float(request.POST.get('quantity', None))    
    r = int(request.POST.get('rolli', None))

    if(p and f and q and r):
        chart_item = ChartItem(chart = chart, product = p, finish = f , quantity = q ,boxes = r, note = c)    
        chart_item.save()
        return render(request, "include/chart.html", {"charts": charts})        
    data = {'html_errors' : 'Wrong Finish'}
    return JsonResponse(data, safe=False, status = 500)       


def compute_price(request):

    product = request.POST.get('product', None)
    finish = request.POST.get('finish', None)
    cut = request.POST.get('cut', None)

    
    cut_j = json.loads(cut)
    wall_h = int(cut_j["wall"]["height"][:-2])
    wall_w = int(cut_j["wall"]["width"][:-2])


    paper_width = 0
    rolls = 0
    tot_price = 0
    m2 = 0

    if int(finish) == 0:
        paper_width = 50
        sm_price = 49

    elif int(finish) == 1:
        paper_width = 50

    elif int(finish) == 2:
        paper_width = 65

    elif int(finish) == 3:
        paper_width = 95
        sm_price = 69

    else :
        data = {'html_errors' : 'Wrong Finish'}
        return JsonResponse(data, safe=False, status = 500)       
    
    wall_h = wall_h+10
    rolls = math.ceil(float(wall_w)/ float(paper_width) ) +1
    m2 = float(wall_h)/ 100.0 *(float(rolls * paper_width)) / 100.0
    
    tot_price = sm_price *m2
    data = {'tot_price': tot_price,'m2':m2,'rolli':rolls,'cut_val':cut}
    
    return JsonResponse(data, status = 200)


def capsule_product(request, _name, product_code, chi_form = None ):    
    
    try: 
        product = Product.active.get(code = product_code )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message":"The product you asked to view is not existing",}) 

    influencer = Influencer.objects.get(name__slug  = _name )

    
    if request.is_ajax():
        add_chart_capsule(request)
        return render(request)


    return render(request, "product_capsule.html",{
        "product"   :product,
        "influencer":influencer,
        })