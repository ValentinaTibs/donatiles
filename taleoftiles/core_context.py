from django.core.exceptions import ObjectDoesNotExist

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

    if context.user.is_authenticated:
        try:
            sampler = Chart.objects.get(user  = context.user, is_sample = True)
        except ObjectDoesNotExist:
            sampler = None
        try: 
            chart = Chart.objects.get(user  = context.user, is_sample = False)
        except ObjectDoesNotExist:
            chart = None

    elif context.session.exists(context.session.session_key):
        
        try:
            sampler = Chart.objects.get(session_id  = context.session.session_key, is_sample = True)
        except ObjectDoesNotExist:
            sampler = None
        try: 
            chart = Chart.objects.get(session_id  = context.session.session_key, is_sample = False)
        except ObjectDoesNotExist:
            chart = None
    else:
        sampler = None
        chart   = None
            
    return {'sampler': sampler,'chart':chart,
    'user':context.user,
    'loginform':LoginForm, 'signupform':RegisterForm,
    'session' : context.session.session_key
    } 

