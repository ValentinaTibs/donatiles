from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from django.db.models import Q 
from taleoftiles.utils  import compute_single_price, compute_sm_price

from taleoftiles.models import Tag, Product, Catalogue
from layout.models      import Element
from blog.models        import Post
from CRM.models        import Chart

from CRM.forms          import AddChartForm
from django.db.models import Count

def index(request):  
    home_elems      = Element.objects.filter(tag__parent__slug = 'home', public = True)
    home_tags       = Tag.objects.filter(in_home = True, public = True)
    secondary_post  = Post.active.get(tags__slug='secondary-post')
    main_post       = Post.active.get(tags__slug='main-post')

    return render(request, "home.html",{
        'layout_elems'  : home_elems,
        'tags'          : home_tags,
        'secondary_post': secondary_post,
        'main_post'     : main_post
        })


from django.http import JsonResponse
from django.shortcuts import render

from django.core import serializers


from django.views.generic.list import ListView

class catalogue(ListView):
    active_tags = None
    url_data = ''

    model = Product 
    
    paginate_by = 300
    context_object_name = 'products'
    template_name = 'catalogue.html'
    #2do put here a custom ordering
    ordering = ['name']    

    #2do maybe here using the self instance might save us time
    def post(self, request):

        if self.request.is_ajax():
            url_data =[]
            url_data_string = request.POST.get('url_data', None)
            if url_data_string:
                url_data = url_data_string.split('_')
            the_filter = request.POST.get('toggleFilter', '')
            
            if (the_filter in url_data):
                url_data.remove(the_filter)
            else:
                url_data.append(the_filter)
            
            #2do this must became a function
            tag_query = Q()
            tag_len = 0
            for value in url_data:
                tag_query = tag_query | Q(slug = value)
                tag_len = tag_len + 1

            all_tags = Tag.objects.filter(in_catalogue = True ,parent__isnull = True, public = True).in_bulk(field_name='slug')   
            active_tags = None

            if tag_len == 0 :
                products = Product.objects.filter(is_active=True)
            else:
                active_tags = Tag.objects.filter(tag_query)
                products = Product.objects.filter(is_active=True,tags__in=active_tags).annotate(num_tags=Count('tags')).filter(num_tags=tag_len).distinct().all()
            
            return render(request, "cataloguegrid.html", {"products": products,"active_tags" : active_tags,'tags':all_tags,'url_data':'_'.join(url_data) })

    def get_context_data(self, **kwargs):
        
        context = super(catalogue, self).get_context_data(**kwargs)
        try: 
            cat = Catalogue.objects.get(active = True)
        except ObjectDoesNotExist:
            return render(request, "404.html",{"message":"There is no active catalogue",})

        
        context['tags']         = self.all_tags.in_bulk(field_name='slug')
        context['active_tags']  = self.active_tags
        context['url_data']     = self.url_data

        return context
    
    def get_queryset(self):
        if self.request.method == 'GET':
            self.url_data = self.request.GET.get('filters', '')  
            self.all_tags = Tag.objects.filter(in_catalogue = True, parent__isnull = True, public = True)
            if not self.url_data :
                return Product.objects.filter(is_active=True)

            tag_query = Q()
            tag_len = 0

            for value in self.url_data.split('_'):
                tag_query = tag_query | Q(slug = value)
                tag_len = tag_len + 1
            if tag_len == 0 :
                return Product.objects.filter(is_active=True)
            
            self.active_tags =  Tag.objects.filter( tag_query,public=True)
            return Product.objects.filter(is_active=True,tags__in=self.active_tags).annotate(num_tags=Count('tags')).filter(num_tags=tag_len).distinct()


def compute_price(request, product_id):
    return redirect(request.META.get('HTTP_REFERER'))

def product(request, product_code, chi_form = None ):    
    
    try: 
        product = Product.active.get(code = product_code )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message":"The product you asked to view is not existing",}) 

    #for all product in the same series that are not support and not itself
    related_series  = Product.active.filter(tags = product.get_tag('serie'),support_to = None).exclude(pk = product.pk)
    
    chi_form = AddChartForm(request.POST or {'product':product.pk,} ,  None)
    
    query = Q()
    if request.user.is_authenticated:
        query = Q(user = request.user) 
    else:
        if not request.session.exists(request.session.session_key):
            request.session.create()     
        query = Q(session_id  = request.session.session_key) 

    try: 
        chart = Chart.objects.filter( query , completion_status = 's').first()
    except ObjectDoesNotExist:
        chart = Chart(session_id  = request.session.session_key)
        if request.user.is_authenticated:
            chart.user = request.user
        chart.save()
    
    price = 0
    errors = None
    if request.method == 'POST':
    
        if chi_form.is_valid() and "save_it" in request.POST:
            chart_item = chi_form.save(commit=False)        
            price = chart_item.price()
            chart_item.save_price = chart_item.price()
            chart_item.chart = chart
            chart_item.save()
                    
        errors = (chi_form.errors)

    # if request.method == 'POST':
    #     
    #     if chi_form.is_valid():
    #         print("we are valid")
    #         chart_item = chi_form.save(commit=False)
    #         if  "save_it" in request.POST:
    #             chart_item.chart = chart
    #             chart_item.save()
    #             print("we didnt saved")
            
    
    return render(request, "product.html",{
        "product":product,
        "products_series":related_series,
        "chi_form" : chi_form, 
        "errors" : errors,
        "price":price
        })
