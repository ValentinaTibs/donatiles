from django.core.exceptions import ObjectDoesNotExist

from taleoftiles.models import Tag
from CRM.models import Chart
from CRM.forms 	import LoginForm, RegisterForm

def category_menu(context):
    cats = Tag.objects.filter(public = True, in_menu = True)
    return {'menu_cats': cats} 


def user_menu(context):

	if context.session.exists(context.session.session_key):
		
		try:
			sampler = Chart.objects.get(session_id  = context.session.session_key, is_sample = True)
		except ObjectDoesNotExist:
			sampler = None
		try: 
			chart = Chart.objects.get(session_id  = context.session.session_key, is_sample = False)
		except ObjectDoesNotExist:
			chart = None			
	return {'sampler': sampler,'chart':chart,
	'user':context.user,
	'loginform':LoginForm, 'signupform':RegisterForm} 

