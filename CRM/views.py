from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login

from CRM.models         import Chart, ChartItem, Sampler, Sample, Shipping, Order
from CRM.models         import Profile
from taleoftiles.models import Product
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

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
   
    try:
        prev_data = Shipping.objects.get( user = profile)
    except ObjectDoesNotExist:
        prev_data = Shipping(email = request.user.email )
    shipping_form = ShippingForm(instance=prev_data)
    if request.method == 'POST':
        shipping_form = ShippingForm(request.POST, instance=prev_data)
        
        if shipping_form.is_valid():
            new_shipping = shipping_form.save()
        
    return render(request, "account.html", {'profile':profile,'shipping_form':shipping_form})

def summary(request, id_ ):

    try:
        order = Order.objects.get( internal_tracking_id = id_)
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message": "This order does not exist" })
    
    # if order.is_paid():
    #     return redirect('payment', id_ = order.internal_tracking_id)
            
    return render(request, "summary.html", {'order':order,'prv_page':request.session['prev_page']})     

def order(request, id_ ):
    
    try:
        order = Order.objects.get( internal_tracking_id = id_)
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message": "This order does not exist" })
                
    return render(request, "order.html", {'order':order})     


def payment(request, id_):

    try:
        order = Order.objects.get( internal_tracking_id = id_)
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message": "This order does not exist" })
    
    #2do per ragioni di sicurezza questo aggiornamento si dovrebbe fare solo se arrivo a questa pagina con una post
    if order.is_sampler:
        for sampler in order.sampler.all():
            if order.final_payment <= 0:
                sampler.completion_status = 'p'
            else:
                sampler.completion_status = 'c'    
            sampler.save()
    else:
        for chart in order.charts.all():
            chart.completion_status = 'c'
            chart.save()
    return render(request, "payment.html", {'order':order,'prv_page': request.session['prev_page']})   

    
def create_one_time_password():
    get_random_string(length=8)

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

        #2do check se la mail e gia inserita tra gli utenti invitarlo a loggarsi
        if shipping_form.is_valid():
            new_shipping = shipping_form.save()
            if request.user.is_authenticated:
                new_shipping.user = request.user.profile
                new_shipping.save()
            else: 
                new_user = User.objects.create_user( username=new_shipping.email, email=new_shipping.email,password=create_one_time_password()) 
                new_user.set_unusable_password()
                new_user.save()
                da_user = Profile( user = new_user)        
                result = da_user.save()                
                login(request, new_user)
                        
            order.final_payment = order.total()
            #order.shipping = new_shipping
            order.save()

            return redirect('payment', id_ = order.internal_tracking_id)
        
    return render(request, "shipping.html", {'form':shipping_form,'order':order,'prv_page': request.session['prev_page']})   


def add_sample_order(request):
    
    query = Q()
    if request.user.is_authenticated:
        query = Q(user = request.user) 
    else:
        query = Q(session_id  = request.session.session_key) 

    the_charts = Sampler.objects.filter( query,completion_status = 's' )
    # se nessun carrello ha un ordine fai un ordine - 
    if not the_charts or the_charts.count() <= 0 or not the_charts.first().order :
        order = Order()
        order.is_sampler = True
        order.save()

    else :         
        # altrimenti prendi l'ordine del primo dei carrelli 
        good_chart = the_charts.first()
        order = good_chart.order

    # assegna questo ordine a ciascun carrello presente
    for chart in the_charts:
        if not chart.order:
            chart.order = order
            chart.save()
        
    if request.method == 'GET':
        request.session['prev_page'] = request.GET['prv']

    return redirect('summary', id_ = order.internal_tracking_id)


def add_order(request, is_sample):
    query = Q()
    if request.user.is_authenticated:
        query = Q(user = request.user) 
    else:
        query = Q(session_id  = request.session.session_key) 
    order = None
    the_charts = Chart.objects.filter( query,completion_status = 's')
    # se nessun carrello ha un ordine fai un ordine - 
    if not the_charts or the_charts.count() <= 0 or not the_charts.first().order:
        order = Order()
        order.save()
    else : 
        # altrimenti prendi l'ordine del primo dei carrelli 
        good_chart = the_charts.first()
        order = good_chart.order

    # assegna questo ordine a ciascun carrello presente
    for chart in the_charts:
        if not chart.order:
            chart.order = order
            chart.save()
        
    if request.method == 'GET':
        request.session['prev_page'] = request.GET['prv']

    return redirect('summary', id_ = order.internal_tracking_id)

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


def ajax_del_sample(request):
    if request.is_ajax():
        product_code = request.POST.get('product_code', None)
        
        try: 
            product = Product.objects.get(code = product_code )
        except ObjectDoesNotExist:
            return render(request, "include/sampler.html",{"message": "There is no product with code " + product_code})

        if request.user.is_authenticated:
            query = Q(sampler__user = request.user) 
        elif request.session.exists(request.session.session_key):
            query = Q(sampler__session_id  = request.session.session_key) 

        try: 
            sample = Sample.objects.get(query, product = product, status = 'ok' )
        except ObjectDoesNotExist:
            return render(request, "include/sampler.html",{"message": "Removing something that wasnt in your sampler " + Sample.product,})
        sample.status = 'ru'
        sample.save()

        return render(request, "include/sampler.html", {"all_samples": sample.sampler,'user':request.user })


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
    
    #retrieving an already ongoing sampler
    try: 
        sampler = Sampler.objects.get( query , completion_status = 's')
    except ObjectDoesNotExist:
        sampler = Sampler(session_id  = request.session.session_key)
        if request.user.is_authenticated:
            sampler.user = request.user
        sampler.save()

    #avoiding double insertion
    try:
        sample = Sample.objects.get(sampler = sampler, product = product, status = 'ok')
        return render(request, "include/sampler.html",{"message": "Already in your sample "})
    except ObjectDoesNotExist:
        remove_stat = 'ok'       
        if remove_stat == 'ok':
            sample = Sample(sampler  = sampler, product = product, status = remove_stat)
            sample.save()

    return redirect('product', product_code= product_code )


def ajax_add_sample(request, ):

    if request.is_ajax():
        product_code = request.POST.get('product_code', None)
        
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
        
        #retrieving an already ongoing sampler
        try: 
            sampler = Sampler.objects.get( query , completion_status = 's')
        except ObjectDoesNotExist:
            sampler = Sampler(session_id  = request.session.session_key)
            if request.user.is_authenticated:
                sampler.user = request.user
            sampler.save()
        if (sampler.all_samples().count() > 4):
            return render(request, "include/sampler.html", {"all_samples": sampler,'user':request.user })

        #avoiding double insertion
        try:
            sample = Sample.objects.get(sampler = sampler, product = product, status = 'ok')
        except ObjectDoesNotExist:
            remove_stat = 'ok'
            if remove_stat == 'ok':
                sample = Sample(sampler  = sampler, product = product, status = remove_stat)
                sample.save()       
                    
        return render(request, "include/sampler.html", {"all_samples": sampler,'user':request.user })
    

def del_chart(request, item_id):

    if request.user.is_authenticated:
        query = Q(chart__user = request.user) 
    elif request.session.exists(request.session.session_key):
        query = Q(chart__session_id  = request.session.session_key) 

    try: 
        chart_item = ChartItem.objects.get(query, pk = item_id, status = 'ok' )
    except ObjectDoesNotExist:
        return render(request, "404.html",{"message": "Removing something that wasnt in your sampler ",})
    chart_item.delete()
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

