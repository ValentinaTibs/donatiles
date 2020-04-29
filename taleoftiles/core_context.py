from taleoftiles.models import Tag
from CRM.models import Chart

def category_menu(context):
    cats = Tag.objects.filter(public = True, in_menu = True)
    return {'menu_cats': cats} 


def user_menu(context):
	sampler = ()
	chart = ()

	if context.session.exists(context.session.session_key):
		all_session_charts = Chart.objects.filter(session_id  = context.session.session_key )
		sampler = all_session_charts.filter(is_sample = True)	
		chart = all_session_charts.filter(is_sample = False)

	return {'sampler': sampler,'chart':chart} 
