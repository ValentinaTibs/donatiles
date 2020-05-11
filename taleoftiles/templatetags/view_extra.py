import datetime
from django import template

register = template.Library()

@register.filter(name = 'starts_with')
def starts_with(expected,actual):
    return actual.startswith(expected);

@register.filter
def clean(value):
    return value.replace('-',' ')

@register.filter
def get_elem(queryset, key):
    elem = queryset.get(tag__slug=key)
    return(elem)

@register.filter
def filter_tags(queryset, key):
    elems = queryset.filter(parent__slug=key)
    return(elems)

@register.simple_tag
def define(val=None):
  return val

@register.filter
def is_in_sample(chart, product):
    if chart: 
        return chart.is_in_sample(product).count() > 0
    return False

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
