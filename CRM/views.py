from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from CRM.models         import Chart, ChartItem, Shipping, Order
from CRM.models         import Profile
from taleoftiles.models import Product

from CRM.forms import RegisterForm,ShippingForm

from django.db.models import Q 

#@login_required(redirect_field_name='my_redirect_field')
def account(request):
    if not request.user.is_authenticated:
        return render(request, "404.html",{"message": "Page forbidden for not autenticated user - please login"})
    try: 
        profile = Profile.objects.get(user = request.user )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message": "There is no user for such profile " })
   
    return render(request, "account.html", {'profile':profile})

def summary(request):

    if request.method == 'GET':
        prv_page = request.GET['prv']

    query = Q()
    if request.user.is_authenticated:
        query = Q(user = request.user) 
    else:
        query = Q(session_id  = request.session.session_key) 
    
    charts   = Chart.active.filter( query )
    for chart in charts:
        chart.status = 'i1'
        chart.save()
    return render(request, "summary.html", {'charts':charts,'prv_page':prv_page})   

def payment(request, id_):
    try:
        new_order = Order.objects.get( pk = id_)
    except ObjectDoesNotExist:
            return render(request, "404.html",{"message": "This order does not exist" })
    return render(request, "payment.html", {'order':new_order,'prv_page':None})   

def shipping(request):

    if request.method == 'GET':
        prv_page = request.GET['prv']

    query = Q()
    prev_data = None

    if request.user.is_authenticated:
        query = Q(user = request.user)
        try:
            prev_data = Shipping.objects.get( user__user = request.user)
        except ObjectDoesNotExist:
            prev_data = None
    else:
        query = Q(session_id  = request.session.session_key) 
    
    charts   = Chart.active.filter( query )
    shipping_form = ShippingForm(instance=prev_data)

    if request.method == 'POST':
        shipping_form = ShippingForm(request.POST, instance=prev_data)

        #2do mettere qui controlli sicurezza
        prv_page = request.POST['prv']

        if shipping_form.is_valid():
            shipping_form.save()
            
            new_order = Order()
            new_order.save()

            for chart in charts:
                chart.status = 'c'
                chart.order = new_order
                chart.save()

            #ok to keep this as this since is not possible to reach this page from anywhereselle
            return render(request, "payment.html", {'order':new_order,'prv_page':prv_page})   

    for chart in charts:
        chart.status = 'i2'
        chart.save()

    return render(request, "shipping.html", {'form':shipping_form,'prv_page':prv_page})   


def add_user(request):

    form = RegisterForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            new_user = form.save()
            da_user = Profile(user = new_user)        
            da_user.save()
            #login(request, new_user)
            #???user = authenticate(username=new_user.username, password=new_user.password)
    
    return redirect(request.META.get('HTTP_REFERER'))

def del_chart(request, product_slug, is_sample):
    sess_k =request.session.session_key

    try: 
        chart_item = ChartItem.objects.get(chart__session_id  = sess_k, chart__is_sample = is_sample, 
            product__publication__slug = product_slug, status = 'ok' )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message": "Removing something that wasnt in your chart/sampler " + product_slug,})
    chart_item.status = 'ru'
    chart_item.save()
    return redirect(request.META.get('HTTP_REFERER'))

def add_sample(request, product_slug):
    
    try: 
        product = Product.objects.get(publication__slug = product_slug )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message": "There is no product with code " + product_slug,})

    if not request.session.exists(request.session.session_key):
        request.session.create() 

    try: 
        chart = Chart.objects.get( session_id  = request.session.session_key, is_sample = True )
    except ObjectDoesNotExist:
        chart = Chart(session_id  = request.session.session_key, is_sample = True)
        if request.user.is_authenticated:
            chart.user = request.user
        chart.save()

    try:
        chart_item = ChartItem.objects.get(chart = chart, product = product, status = 'ok')
    except ObjectDoesNotExist:
        remove_stat = 'ok'
        if (chart.num_prods() > 4):
            remove_stat = 'le'
        #this might cause db collapse
        if (not product.is_samplable):
            remove_stat = 'ns'          
        chart_item = ChartItem(chart  = chart, product = product, status = remove_stat)
        chart_item.save()

    return redirect('product', product_slug= product_slug )

def add_chart(request, product_slug):

    try: 
        product = Product.objects.get(publication__slug = product_slug )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message": "There is no product with code " + product_slug,})
    
    if not request.session.exists(request.session.session_key):
        request.session.create() 

    try: 
        chart = Chart.objects.get(session_id  = request.session.session_key, is_sample = False )
    except ObjectDoesNotExist:
        chart = Chart(session_id  = request.session.session_key, is_sample = False)
        if request.user.is_authenticated:
            chart.user = request.user
        chart.save()

    try:
        chart_item = ChartItem.objects.get(chart__pk  = chart.pk, product__pk = product.pk, status = 'ok',)
    except ObjectDoesNotExist:
        chart_item = ChartItem(chart = chart, product = product)
        chart_item.save()

    return redirect('product', product_slug= product_slug )