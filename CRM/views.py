from django.shortcuts import render, redirect

from CRM.models import Chart, ChartItem

from CRM.models import Profile

from CRM.forms import RegisterForm

from taleoftiles.models import Product

from django.core.exceptions import ObjectDoesNotExist


def add_user(request):

	form = RegisterForm(request.POST or None, request.FILES or None)

	if request.method == 'POST':
		if form.is_valid():
			new_user = form.save()
			da_user = Profile(user = new_user)        
            #???user = authenticate(username=new_user.username, password=new_user.password)
            #login(request, new_user)
			
	return redirect(request.META.get('HTTP_REFERER'))

def del_chart(request, product_slug, is_sample):
	sess_k =request.session.session_key
	try: 
		chart_item = ChartItem.objects.get(chart__session_id  = sess_k, chart__is_sample = is_sample, product__publication__slug = product_slug, status = 'ok' )
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

	session_loc_id = request.session._get_or_create_session_key()

	try: 
		chart = Chart.objects.get(session_id  = session_loc_id, is_sample = True )
	except ObjectDoesNotExist:
		chart = Chart(session_id  = session_loc_id, is_sample = True)
		chart.save()

	try:
		chart_item = ChartItem.objects.get(chart = chart, product = product, status = 'ok')
	except ObjectDoesNotExist:
		remove_stat = 'ok'
		if (chart.num_prods() > 4):
			remove_stat = 'le'
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

	session_loc_id = request.session._get_or_create_session_key()

	try: 
		chart = Chart.objects.get(session_id  = session_loc_id, is_sample = False )
	except ObjectDoesNotExist:
		chart = Chart(session_id  = session_loc_id, is_sample = False)
		chart.save()

	try:
		chart_item = ChartItem.objects.get(chart__pk  = chart.pk, product__pk = product.pk, status = 'ok',)
	except ObjectDoesNotExist:
		chart_item = ChartItem(chart  = chart, product = product)
		chart_item.save()

	return redirect('product', product_slug= product_slug )