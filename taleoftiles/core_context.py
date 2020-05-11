from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from taleoftiles.models import Tag
from CRM.models import Chart
from CRM.forms  import LoginForm, RegisterForm

#####  -----------
# mantaining the same session key after authentication process
from django.contrib.sessions.backends.db import SessionStore as DbSessionStore

class SessionStore(DbSessionStore):
    def cycle_key(self):
        pass
#####  -----------        

def category_menu(context):
    cats = Tag.objects.filter(public = True, in_menu = True)
    return {'menu_cats': cats} 

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
    sampler = Chart.samples.filter  ( query ).first()

    return {'sampler': sampler,'charts':charts,
        'loginform':LoginForm, 'signupform':RegisterForm,
        'session' : context.session.session_key
    } 

