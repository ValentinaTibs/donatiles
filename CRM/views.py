from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login

from CRM.models         import Chart, ChartItem, Sampler, Sample, Shipping, Order
from CRM.models         import Profile
from taleoftiles.models import Product

from CRM.forms import RegisterForm,ShippingForm,NewChartItemForm

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



def summary(request, is_sample = False):
    if request.method == 'GET':
        prv_page = request.GET['prv']

    query = Q()
    if request.user.is_authenticated:
        query = Q(user = request.user) 
    else:
        query = Q(session_id  = request.session.session_key) 

    charts = []
    sampler = None
    if is_sample:
        sampler = Sampler.objects.get( query )
    else:
        charts = Chart.objects.filter( query )    
    
    total = 0
    for chart in charts:
        chart.status = 'i1'
        chart.save()
        total += chart.total_price()
        
    return render(request, "summary.html", {'charts':charts,'sampler':sampler,'prv_page':prv_page,
        'total':total})     
    
def payment(request, id_):
    try:
        new_order = Order.objects.get( pk = id_)
    except ObjectDoesNotExist:
            return render(request, "404.html",{"message": "This order does not exist" })
    return render(request, "payment.html", {'order':new_order,'prv_page':None})   

#2do we might pass the chart or sampler here
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

        #2do mettere qui controlli sicurezza (quale sicurezza?)
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
            #new_user.is_active = False
            #new_user.set_unusable_password()
            new_user.save()
            da_user = Profile( user = new_user)        
            da_user.save()
            login(request, new_user)
            
    #2do add to the redirect the form error 
    return redirect(request.META.get('HTTP_REFERER'))

def del_sample(request, item_id):

    if request.user.is_authenticated:
        query = Q(sampler__user = request.user) 
    elif request.session.exists(request.session.session_key):
        query = Q(sampler__session_id  = request.session.session_key) 

    try: 
        sample = Sample.objects.get(query, pk = item_id, status = 'ok' )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message": "Removing something that wasnt in your sampler " + Sample.product,})
    sample.status = 'ru'
    sample.save()
    return redirect(request.META.get('HTTP_REFERER'))

def add_sample(request, product_code):
    
    try: 
        product = Product.objects.get(code = product_code )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message": "There is no product with code " + product_code,})

    query = Q()
    if request.user.is_authenticated:
        query = Q(user = request.user) 
    else:
        if not request.session.exists(request.session.session_key):
            request.session.create()     
        query = Q(session_id  = request.session.session_key) 
    try: 
        sampler = Sampler.objects.get( query )
    except ObjectDoesNotExist:
        sampler = Sampler(session_id  = request.session.session_key)
        if request.user.is_authenticated:
            sampler.user = request.user
        sampler.save()
    try:
        sample = Sample.objects.get(sampler = sampler, product = product, status = 'ok')
    except ObjectDoesNotExist:
        remove_stat = 'ok'
        #2do this might cause db collapse if saved 
        if (sampler.all_samples().count() > 4):
            remove_stat = 'le'
        #2do this might cause db collapse if saved
        if (not product.is_samplable):
            remove_stat = 'ns'          
        if remove_stat == 'ok':
            sample = Sample(sampler  = sampler, product = product, status = remove_stat)
            sample.save()

    return redirect('product', product_code= product_code )

def del_chart(request, item_id):

    if request.user.is_authenticated:
        query = Q(chart__user = request.user) 
    elif request.session.exists(request.session.session_key):
        query = Q(chart__session_id  = request.session.session_key) 

    try: 
        chart_item = ChartItem.objects.get(query, pk = item_id, status = 'ok' )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message": "Removing something that wasnt in your sampler " + ChartItem.product,})
    chart_item.status = 'ru'
    chart_item.save()
    return redirect(request.META.get('HTTP_REFERER'))


def add_chart(request, product_code):

    chi_form = NewChartItemForm(request.POST or None, request.FILES or None)
    if not request.session.exists(request.session.session_key):
        request.session.create() 

    chart = Chart.objects.filter(session_id  = request.session.session_key ).first()

    if not chart:
        chart = Chart(session_id  = request.session.session_key)
        if request.user.is_authenticated:
            chart.user = request.user
        chart.save()

    if request.method == 'POST':

        if chi_form.is_valid():
            chart_item = chi_form.save(commit=False)
            chart_item.chart = chart
            chart_item.save()
    return redirect(request.META.get('HTTP_REFERER'))

