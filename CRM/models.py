from django.utils.crypto import get_random_string
from django.db import models
from django.db.models import Count, Q, Sum

from django.utils import timezone

from django.contrib.auth.models import User
from taleoftiles.models import Product
from taleoftiles.utils import COMPLETION_, SHIPPING_, ORDER_, ITEM_, COUNTRIES_


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = False, related_name='profile')
    
class Shipping(models.Model):

    profile = models.ForeignKey(Profile,  blank = True, null = True, on_delete=models.SET_NULL, related_name='shippings' )
    country             = models.CharField(max_length=2, choices=COUNTRIES_, default='t')
    fullname            = models.TextField(max_length=100, blank=True)
    country             = models.TextField(max_length=100, blank=True)
    city                = models.TextField(max_length=100, blank=True)
    CAP                 = models.TextField(max_length=10, blank=True)
    shipping_address    = models.TextField(max_length=100, blank=True)
    telephone_num       = models.TextField(max_length=30, blank=True)

    is_active           = models.BooleanField(default = True)

class ActiveChartManager(models.Manager):
    def get_queryset(self):
        query = Q(completion_status = 's') | Q(completion_status = 'i1') | Q(completion_status = 'i2') 
        query = (query) & Q( is_sample = False)
        qs = super().get_queryset().filter(query).annotate(
            total = Count('chart_item',filter=Q(chart_item__status='ok')),
            count = Sum('chart_item',filter=Q(chart_item__status='ok'))
        )
        return qs
          
class ActiveSamplesManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().filter(completion_status = 's', is_sample = True).annotate(
            total = Count('chart_item',filter=Q(chart_item__status='ok')),
            count = Sum('chart_item',filter=Q(chart_item__status='ok'))
            )
        return qs

def create_shipping_internal_id():
    return get_random_string(length=32)

class Order(models.Model):
    note = models.TextField(max_length = 200, null = True)

    internal_tracking_id = models.CharField(max_length=100, default = "")
    shipping_tracking_id = models.CharField(max_length=100, default = "")

    order_status        = models.CharField(max_length=2, choices=ORDER_, default='w')
    created_at  = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.internal_tracking_id = create_shipping_internal_id()
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        super().save(*args, **kwargs)  # Call the "real" save() method.


class Chart(models.Model):
    session_id  = models.CharField ( max_length=100, default="", null = True)
    user        = models.ForeignKey( Profile,  blank = True,        null = True, on_delete=models.SET_NULL, related_name='charts' )
    order       = models.ForeignKey( Order, verbose_name="Order",   null = True, on_delete=models.CASCADE,  related_name='charts')

    completion_status   = models.CharField(max_length=2, choices=COMPLETION_, default='s')
    is_sample           = models.BooleanField(default = False)

    created_at  = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()

    objects     = models.Manager() # The default manager.
    active      = ActiveChartManager() # The Active Charts
    samples     = ActiveSamplesManager() # The Active Samples

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super().save(*args, **kwargs)  

    def __str__(self):
        return self.session_id

    def all_samples(self):
        if self.chart_item and self.is_sample:
            return self.chart_item.filter(status = 'ok')
    
    def all_items(self):
        if self.chart_item and (not self.is_sample):
            return self.chart_item.filter(status = 'ok')

class ChartItem(models.Model):
    chart       = models.ForeignKey(Chart,  verbose_name="Charts", null=True, on_delete=models.SET_NULL, related_name='chart_item')
    product     = models.ForeignKey(Product,  verbose_name="Products", null=True, on_delete=models.SET_NULL, related_name='chart_item')
    status     = models.CharField(max_length=2, choices=ITEM_, default='ok')

    quantity    = models.PositiveIntegerField( default=1 )   
    
    created_at  = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.chart.session_id        
   
class Question(models.Model):
    content = models.TextField()
    name    = models.CharField(max_length=100,default = "")
    email   = models.EmailField(max_length=100,default = "")

    modified_at = models.DateTimeField()    
    created_at  = models.DateTimeField("date created",editable=False)
    publish_date = models.DateTimeField("date published", blank = True, null = True, auto_now_add=False)

    reply = models.ForeignKey("self", blank = True, null = True,on_delete=models.SET_NULL, related_name='question' )

    public = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super().save(*args, **kwargs)

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
   