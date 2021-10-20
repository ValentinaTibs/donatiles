from django.shortcuts import render
from taleoftiles.models import Product
# Create your views here.

def index(request):  
    influencer_slug = 'giggilatrottola'
    #products = Product.filter(is_active = True, influencer__slug = influencer_slug).annotate(num_tags=Count('tags')).filter(num_tags=tag_len).distinct().order_by(order_by)
    products = Product.objects.all()[:3]
    return render(request, "capsulette.html",{
        "products": products,
        })