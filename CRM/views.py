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

def summary(request, id_ ):
    
    try:
        order = Order.objects.get( internal_tracking_id = id_)
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message": "This order does not exist" })
    return render(request, "summary.html", {'order':order,'prv_page':request.session['prev_page']})     
    
def payment(request, id_):

    try:
        order = Order.objects.get( internal_tracking_id = id_)
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message": "This order does not exist" })

    if order.is_sampler:
        for sampler in order.sampler.all():
            if order.final_payment <= 0:
                sampler.completion_status = 'p'
            else:
                chart.completion_status = 'c'    
            #sampler.save()
    else:
        for chart in order.charts.all():
            chart.completion_status = 'c'
            #chart.save()
    return render(request, "payment.html", {'order':order,'prv_page': request.session['prev_page']})   

def shipping(request, id_):
    

    query = Q()
    prev_data = None

    try:
        order = Order.objects.get( internal_tracking_id = id_)
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message": "This order does not exist" })
    
    if order.user() :
        try:
            prev_data = Shipping.objects.get( user__user = order.user())
        except ObjectDoesNotExist:
            prev_data = Shipping(email = request.user.email )

    shipping_form = ShippingForm(instance=prev_data)

    if request.method == 'POST':
        shipping_form = ShippingForm(request.POST, instance=prev_data)

        if shipping_form.is_valid():
            new_shipping = shipping_form.save()
            if request.user.is_authenticated:
                new_shipping.user = request.user.profile
                new_shipping.save()            
            order.final_payment = order.total()
            order.save()

            return redirect('payment', id_ = order.internal_tracking_id)
        
    return render(request, "shipping.html", {'form':shipping_form,'order':order,'prv_page': request.session['prev_page']})   

def add_order(request, is_sample = False):

    query = Q()
    if request.user.is_authenticated:
        query = Q(user = request.user) 
    else:
        query = Q(session_id  = request.session.session_key) 

    the_chart = None
    chart_model = None

    if is_sample:
        chart_model = Sampler
    else:
        chart_model = Chart

    try:
        the_chart = chart_model.objects.get( query )
    except ObjectDoesNotExist:
        render(request, "404.html",{"message": "Invalid sampler for user" ,})
    
    if not the_chart.order:
        order = Order()
        if is_sample:
            order.is_sampler = True
        order.save()
        the_chart.order = order
        the_chart.save()
        
    if request.method == 'GET':
        request.session['prev_page'] = request.GET['prv']

    return redirect('summary', id_ = the_chart.order.internal_tracking_id)

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

