import datetime
import pytz

from django import template
from django.urls import translate_url
from taleoftiles.models import Tag

register = template.Library()

@register.filter(name = 'starts_with')
def starts_with(expected,actual):
    return actual.startswith(expected)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
    
@register.filter
def clean(value):
    return value.replace('-',' ')

@register.filter
def get_elem(queryset, key):
    elem = queryset.filter(tag__slug=key,public = True).first()
    if elem:
        return(elem.data())
    else:
        return None

@register.filter
def filter_tags(queryset, key):
    elems = queryset.filter(parent__slug=key, public = True)
    return(elems)


import numpy as np
@register.simple_tag
def woking_days(days):
    the_day = np.busday_offset(np.datetime64('today'), days, roll='forward')
    return the_day.item().strftime('%d.%m.%Y')

@register.filter
def working_days(days):
    return woking_days(days)

@register.simple_tag
def min_price(obj, min_price, *args):
    name = (args)[0]
    the_tag = Tag.objects.get(name = name)
    method = getattr(obj, min_price)
    return method(the_tag.slug)
    
    
@register.filter
def is_in_sample(sample, product):
    if sample: 
        return sample.is_in_sample(product).count() > 0
    return False

@register.filter
def serie(product):
    if product: 
        return product.get_tag("serie")
    return "-"

@register.filter
def colour(product):
    if product: 
        return product.filter_tags("colour")
    return "-"

@register.filter
def formats(product):
    if product: 
        return product.filter_tags("format")
    return "-"

@register.filter
def finishes(product):
    if product: 
        return product.filter_tags("finish")
    return "-"

@register.filter
def styles(product):
    if product: 
        return product.filter_tags("style")
    return "-"

@register.filter
def effects(product):
    if product: 
        return product.filter_tags("effect")
    return "-"

@register.inclusion_tag('include/productthumb.html')
def product_thumb(product):
    return {'product':product}    


@register.simple_tag(takes_context=True)
def change_lang(context, lang=None):    
    return translate_url(context['request'].path, lang)

@register.filter
def order_discount(order):
    return int(order.discount.total_discount(order.chart_price()))
    

# @register.filter(name='check_city') 
# def check_city(user, city_name):
#   guy_name = user.userprofile.centre.related.slug.split('-')[0].capitalize()
#   admin = Group.objects.get(name='Admin') 
#   return True if admin in user.groups.all() else False  
#   return True if guy_name == str(city_name) else False 

#from django.contrib.auth.models import Group

# @register.filter(name='has_group') 
# def has_group(user, group_name): 
#   group = Group.objects.get(name=group_name) 
#   return True if group in user.groups.all() else False 


# @register.filter(name='hasnot_group') 
# def hasnot_group(user, group_name): 
#   group = Group.objects.get(name=group_name) 
#   return False if group in user.groups.all() else True 

# @register.filter
# def get_item_count(dictionary, key):
#     return [len(list(dict(dictionary).get(key))),list(dict(dictionary).get(key))]
