from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse

from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from django.db.models import Q 
from taleoftiles.utils  import compute_single_price, compute_sm_price

from taleoftiles.models import Tag, Product, Catalogue
from layout.models      import Element, MailTemplate
from blog.models        import Post
from CRM.models        import Chart

from CRM.forms          import AddChartForm,WallpaperForm
from django.db.models import Count

def index(request):  
    home_elems      = Element.objects.filter(tag__parent__slug = 'home', public = True)
    home_tags       = Tag.objects.filter(in_home = True, public = True)
    secondary_post  = Post.active.get(tags__slug='secondary-post')
    main_post       = Post.active.get(tags__slug='main-post')
    home_prods      = Product.objects.filter(tags__slug = 'in_home',is_active = True)[:8] 

    return render(request, "home.html",{
        'layout_elems'  : home_elems,
        'tags'          : home_tags,
        'secondary_post': secondary_post,
        'main_post'     : main_post,
        'home_prods'    : home_prods
        })

def catalogue(request):  
    order_by = '-publication__created_at'
    results_limit = 9
    url_data =[]
    page = 1

    if request.method == 'GET':
        do_we_have_filters = request.GET.get('filters', '')
        if do_we_have_filters:
            url_data = [request.GET.get('filters', '')]
        page = request.GET.get('page', 1)
    elif request.method == 'POST':
        url_data_string = request.POST.get('url_data', '')
        url_data = url_data_string.split('_')
        toggle_filter = request.POST.get('toggleFilter', '')
        page = request.POST.get('hidden_page', 1)
        try:
            url_data.remove(toggle_filter)
        except ValueError:
            url_data.append(toggle_filter)

    #removing empty string
    url_data = list(filter(('').__ne__, url_data))
    tag_query = Q()
    tag_len = 0

    for value in url_data:
        tag_query = tag_query | Q(slug = value)
        tag_len = tag_len + 1

    # tags in the catalogue shoulder    
    all_tags = Tag.objects.filter(in_catalogue = True ,parent__isnull = True, public = True).in_bulk(field_name='slug')   
    active_tags = Tag.objects.filter(tag_query,public=True) 
    if tag_len > 0 :      
        products_list = Product.objects.filter(is_active = True, tags__in = active_tags).annotate(num_tags=Count('tags')).filter(num_tags=tag_len).distinct().order_by(order_by)
    else:
        active_tags = []
        products_list = Product.objects.filter(is_active = True).annotate(num_tags=Count('tags')).distinct().order_by(order_by)
    

    # pagination 
    paginator = Paginator(products_list, results_limit )
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, "catalogue.html", {
        "products": products,"active_tags" : active_tags,
        'tags':all_tags,'url_data':'_'.join(url_data) })


def compute_price(request):
    quantity = request.POST.get('quantity', None)
    if quantity and int(quantity) > 0:
        product = Product.active.get(pk = request.POST.get('product', None))
        post_size =request.POST.get('size', None)
        if post_size:
            size = Tag.objects.get(pk = post_size)
        post_finish =request.POST.get('finish', None)
        if post_finish:
            size = Tag.objects.get(pk = post_finish)

        quantity = request.POST.get('quantity')
        price = product.price(size)
        
        definitive_price = compute_sm_price( quantity, request.POST.get('has_frido'),product.price(size.slug), product.m2_box(size.slug),product.weight_box(size.slug))
        
        data = {'tot_price': definitive_price}
        return JsonResponse(data, safe=False) 
    return JsonResponse({})   

def product(request, product_code, chi_form = None ):    
    
    try: 
        product = Product.active.get(code = product_code )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message":"The product you asked to view is not existing",}) 

    #for all product in the same series that are not support and not itself
    serie = tags = product.get_tag('serie')
    if serie:
        related_series  = Product.active.filter(tags = product.get_tag('serie'),support_to = None).exclude(pk = product.pk)
    

    if product.is_wallpaper():   
        wallpaper_form = WallpaperForm(request.POST or {'product':product.pk,} ,  None)
        if request.is_ajax():
            if  wallpaper_form.is_valid() :
                new_mail = MailTemplate()
                new_mail.send_wallpaper_req(request, 
                    wallpaper_form.cleaned_data['email'], 
                    wallpaper_form.cleaned_data['width'], 
                    wallpaper_form.cleaned_data['height'], 
                    wallpaper_form.cleaned_data['notes'],
                    wallpaper_form.cleaned_data['name_surname'],  
                    wallpaper_form.cleaned_data['telephone'])
            else:
                data = {'html_errors' : wallpaper_form.errors}
                print(data)
                return JsonResponse(data, safe=False, status = 500)            
            return JsonResponse({'data':'success'}, status = 200)
        chi_form = AddChartForm({'product':product.pk,} ,  None)
        return render(request, "product_wallpaper.html",{
            "product":product,
            "products_series":related_series,
            "chi_form" : chi_form,
            "wallpaper_form" : wallpaper_form
            })

    chi_form = AddChartForm(request.POST or {'product':product.pk,} ,  None)
 
    query = Q()
    price = 0
    errors = None
    if request.is_ajax():
        if chi_form.is_valid() :
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
                
            chart_item = chi_form.save(commit=False)        
            chart_item.save_price = chart_item.price()
            chart_item.chart = chart
            chart_item.boxes = chart_item.compute_num_boxes()
            chart_item.save()
            
            return render(request, "include/chart.html", {"charts": charts})
        #2do put here rendering of errors
        else:
            errors = chi_form.errors
                        
    return render(request, "product.html",{
        "product":product,
        "products_series":related_series,
        "chi_form" : chi_form, 
        "errors" : errors,
        "price":price
        })
