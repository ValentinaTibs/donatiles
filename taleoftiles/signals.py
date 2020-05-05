from CRM.models import Chart
#### ------- Move this to SIgnals.py
from django.contrib.auth.signals import user_logged_in

def pour_charts(sender, user, request, **kwargs):
    session_loc_id = request.session.session_key
    
    for chart in Chart.active.filter( user = user): 
        chart.session_id = session_id
        chart.save()

    for chart in Chart.objects.filter( session_id  = session_loc_id): 
        chart.user = user
        chart.save()

user_logged_in.connect(pour_charts)

#####  --------------
