from django.shortcuts import render, redirect

from CRM.models import Chart, ChartItem
from taleoftiles.models import Product

from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def del_chart(request, product_slug):
	sess_k =request.session.session_key
	try: 
		chart_item = ChartItem.objects.get(chart__session_id  = sess_k, product__publication__slug = product_slug, status = 'ok' )
	except ObjectDoesNotExist:
		return render(request, "404.html",{"message": "Removing something that wasnt in your sampler " + product_slug,})
	chart_item.status = 'ru'
	chart_item.save()
	return redirect(request.META.get('HTTP_REFERER'))

def add_chart(request, product_slug):

	try: 
		product = Product.objects.get(publication__slug = product_slug )
	except ObjectDoesNotExist:
		return render(request, "404.html",{"message": "There is no product with code " + product_slug,})

	session_loc_id = request.session._get_or_create_session_key()

	try: 
		chart = Chart.objects.get(session_id  = session_loc_id )
	except ObjectDoesNotExist:
		chart = Chart(session_id  = session_loc_id, is_sample = True)
		chart.save()

	try:
		chart_item = ChartItem.objects.get(chart__pk  = chart.pk, product__pk = product.pk, status = 'ok',)
	except ObjectDoesNotExist:
		remove_stat = 'ok'
		if (chart.num_prods >= 4):
			remove_stat = 'le'
		if (not product.is_samplable):
			remove_stat = 'ns'			
		chart_item = ChartItem(chart  = chart, product = product, status = remove_stat)
		chart_item.save()

	return redirect('product', product_slug= product_slug )

def add_sample(request, product_slug):

	try: 
		product = Product.objects.get(publication__slug = product_slug )
	except ObjectDoesNotExist:
		return render(request, "404.html",{"message": "There is no product with code " + product_slug,})

	session_loc_id = request.session._get_or_create_session_key()

	try: 
		chart = Chart.objects.get(session_id  = session_loc_id )
	except ObjectDoesNotExist:
		chart = Chart(session_id  = session_loc_id, is_sample = is_sample)
		chart.save()

	try:
		chart_item = ChartItem.objects.get(chart__pk  = chart.pk, product__pk = product.pk, status = 'ok',)
	except ObjectDoesNotExist:
		chart_item = ChartItem(chart  = chart, product = product)
		chart_item.save()

	return redirect('product', product_slug= product_slug )