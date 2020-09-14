from django.shortcuts import render, redirect
from django.http import HttpResponse
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

def custom_merge(unit1, unit2):
   # Merge dictionaries and concat values of same keys if list
   out = {**unit1, **unit2}
   for key, value in out.items():
       if key in unit1 and key in unit2 :
               out[key] = value + unit1[key]
   return out


from django.views.generic.list import ListView

class catalogue(ListView):
    model = Product 
    paginate_by = 6
    context_object_name = 'products'
    template_name = 'productthumb.html'
    ordering = ['name']

    def get_context_data(self, **kwargs):
        context = super(catalogue, self).get_context_data(**kwargs)

        try: 
            cat = Catalogue.objects.get(active = True)
        except ObjectDoesNotExist:
            return render(request, "404.html",{"message":"There is no active catalogue",})
        context['tags'] = cat.tags()        
        return context
    
    def get_queryset(self):
        #return Product.objects.filter(lab__acronym=self.kwargs['lab'])
        return Product.objects.filter(is_active=True)


# def catalogue(request, the_filter = None):

#     catalogue_prod = Product.active.filter(available = True)
#     query_dict  = {}
#     query_items = {}
#     try: 
#         cat = Catalogue.objects.get(active = True)
#     except ObjectDoesNotExist:
#         return render(request, "404.html",{"message":"There is no active catalogue",})

#     if the_filter:
#         try: 
#             tag = Tag.objects.get(slug = the_filter)
#         except ObjectDoesNotExist:
#             return render(request, "404.html",{"message":"There is no active catalogue",})        
        
#         query_dict = custom_merge(query_dict, {tag.parent.slug:[the_filter]})

#     if request.method == 'POST':
#         query_dict = custom_merge(query_dict,(dict(request.POST.lists()))) 

#     for key in query_dict:
#         if key  != 'csrfmiddlewaretoken' and query_dict[key] != [''] :
#             query_items[key] = []
#             for val in query_dict[key]:
#                 query_items[key].append(Tag.objects.get(slug=val))

#     catalogue_tags = cat.tags()
#     catalogue_prod = cat.filter_products(catalogue_prod,query_dict)

#     return render(request, "catalogue.html",{   
#         "tags"          : catalogue_tags,  
#         "products"      : catalogue_prod,
#         "active_tags"   : query_dict,
#         "active_tags_items"   : query_items
#         })


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
