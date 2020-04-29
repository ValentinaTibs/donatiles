from django.shortcuts import render, redirect

from CRM.models import Chart, ChartItem
from taleoftiles.models import Product

from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


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
		chart_item = ChartItem.objects.get(chart__pk  = chart.pk, product__pk = product.pk, removed = False,)
	except ObjectDoesNotExist:
		chart_item = ChartItem(chart  = chart, product = product)
		chart_item.save()

	return redirect('product', product_slug= product_slug )

# try: 
#        product = Product.objects.get(publication__slug  = product_slug )
#    except ObjectDoesNotExist:
#        return render(request, "404.html",{"message":"The product you asked to view is not existing",}) 


