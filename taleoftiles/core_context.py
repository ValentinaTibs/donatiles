from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models import Count

from taleoftiles.models import Tag
from CRM.models import Chart, Sampler
from CRM.forms  import LoginForm, RegisterForm

#####  -----------
# mantaining the same session key after authentication process
from django.contrib.sessions.backends.db import SessionStore as DbSessionStore

class SessionStore(DbSessionStore):
    def cycle_key(self):
        pass
#####  -----------        

def category_menu(context):
    cats = Tag.objects.filter(public = True, child__in_menu = True).distinct()
    return {'menu_cats': cats} 

def footer_menu(context):
    tags_cat = Tag.objects.filter(public = True, child__in_footer = True).distinct()
    return {'footer_tags': tags_cat} 

def user_menu(context):
    query = Q()

    if context.user.is_authenticated:
        query = Q(user = context.user) 
    elif context.session.exists(context.session.session_key):
        query = Q(session_id  = context.session.session_key) 
    else:
        return {'sampler': None,'chart':None, 'user':None,
                'loginform':LoginForm, 'signupform':RegisterForm,
                'session' : context.session.session_key
        } 
    
    charts  = Chart.active.filter   ( query )
    sampler = Sampler.active.filter  ( query ).first()   
    num_ch_i = charts.filter(chart_item__status='ok').aggregate(Count('chart_item'))
    
    return {
            'sampler': sampler, 'charts':charts, 'num_ch_i':num_ch_i['chart_item__count'],
            'loginform':LoginForm, 'signupform':RegisterForm,
            'session' : context.session.session_key
    } 

