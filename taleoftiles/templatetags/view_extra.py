import datetime
#from django.contrib.auth.models import Group

from django import template

register = template.Library()

@register.filter
def clean(value):
	return value.replace('-',' ')

@register.filter
def wpcf_prop(value):
	return CATEGORY[value]


@register.inclusion_tag('release_note.html')
def release_note(notes, type, id ,edit = False ):
	action = '/'+type+'/' +str(id)+'/' +'add_note'+'/'+type+'/'
	return {'notes': notes, 'action':action, 'type': type, 'collapse':False, 'edit': edit}

@register.inclusion_tag('post_small.html')
def post_small(post):
	return {'post_info':post}

@register.inclusion_tag('product_small.html')
def product_small(product):
	return {'product_info':product}

@register.inclusion_tag('product_row.html')
def product_row(product):
	return {'product_info':product}

@register.inclusion_tag('collection_small.html')
def collection_small(collection):
	return {'collection_info':collection}

@register.inclusion_tag('setting_small.html')
def setting_small(setting):
	return {'setting_info':setting}


@register.inclusion_tag('paginator.html')
def paginator(list):
	return {'list':list}

@register.inclusion_tag('page_search.html')
def page_search():
	return {}


@register.inclusion_tag('sidebar_categories.html')
def sidebar_categories():
	return {}


@register.filter
def parse_date(value):
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None

# @register.filter(name='check_city') 
# def check_city(user, city_name):
# 	guy_name = user.userprofile.centre.related.slug.split('-')[0].capitalize()
# 	admin = Group.objects.get(name='Admin') 
# 	return True if admin in user.groups.all() else False  
# 	return True if guy_name == str(city_name) else False 

# @register.filter(name='has_group') 
# def has_group(user, group_name): 
# 	group = Group.objects.get(name=group_name) 
# 	return True if group in user.groups.all() else False 


# @register.filter(name='hasnot_group') 
# def hasnot_group(user, group_name): 
# 	group = Group.objects.get(name=group_name) 
# 	return False if group in user.groups.all() else True 

# @register.filter
# def get_item_count(dictionary, key):
#     return [len(list(dict(dictionary).get(key))),list(dict(dictionary).get(key))]
