import math

from django.utils.crypto import get_random_string
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from django.db.models import Count, Q, Sum

from django.contrib.auth.models import User
from django.dispatch import receiver

from taleoftiles.models import Product, Tag
from taleoftiles.utils  import COUNTRY_LIST, COMPLETION_STATUS, ORDER_STATUS, ITEM_STATUS

from taleoftiles.utils  import compute_price


#### ------- Move this to SIgnals.py
from django.contrib.auth.signals import user_logged_in

def pour_charts(sender, user, request, **kwargs):
    session_loc_id = request.session.session_key
    if not request.session.exists(request.session.session_key):
        return
    session_loc_id = request.session.session_key
    for chart in Chart.active.filter( user = user): 
        chart.session_id = session_loc_id
        chart.save()

    for chart in Chart.objects.filter( session_id  = session_loc_id): 
        chart.user = user
        chart.save()

user_logged_in.connect(pour_charts)

#####  --------------

class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, null = False)
    bio         = models.TextField(max_length=500, blank=True)
    location    = models.CharField(max_length=30, blank=True)
    birth_date  = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username        
   
class Shipping(models.Model):
    #2do this must become a one to Many because we want to keep track of old shippings
    user                = models.OneToOneField(Profile, on_delete=models.CASCADE, null = True)
    fullname            = models.TextField(max_length=100, blank=False)
    country             = models.CharField(max_length=2, choices=COUNTRY_LIST, default='it')
    city                = models.TextField(max_length=100, blank=False)
    CAP                 = models.TextField(max_length=10, blank=False)
    shipping_address    = models.TextField(max_length=100, blank=False)
    telephone_num       = models.TextField(max_length=30, blank=False)
    is_active           = models.BooleanField(default = True)


def create_shipping_internal_id():
    return get_random_string(length=32)

class Order(models.Model):
    note = models.TextField(max_length = 200, null = True)

    internal_tracking_id = models.CharField(max_length=100, default = "")
    shipping_tracking_id = models.CharField(max_length=100, default = "")
    created_at  = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.internal_tracking_id = create_shipping_internal_id()
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        super().save(*args, **kwargs)  # Call the "real" save() method.


class ActiveChartManager(models.Manager):
    def get_queryset(self):
        query = Q(completion_status = 's') | Q(completion_status = 'i1') | Q(completion_status = 'i2') 
        query = query and Q(is_sample = False)
        qs = super().get_queryset().filter(query).annotate(
            total = Count('chart_item',filter=Q(chart_item__status='ok')),
            count = Sum('chart_item',filter=Q(chart_item__status='ok'))
        )
        return qs

# return all charts that are samples and have at least one item 
class ActiveSamplesManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().filter(completion_status = 's', is_sample = True).annotate(
            total = Count('chart_item',filter=Q(chart_item__status='ok')),
            count = Sum  ('chart_item',filter=Q(chart_item__status='ok'))
            )
        return qs
        
class Chart(models.Model):
    session_id  = models.CharField ( max_length=100, default="", null = True)
    user        = models.ForeignKey( User,  blank = True, null = True, on_delete=models.SET_NULL, related_name='charts' )
    order       = models.ForeignKey( Order, verbose_name="Order", null = True, on_delete=models.CASCADE, related_name='charts')

    completion_status   = models.CharField(max_length=2, choices=COMPLETION_STATUS, default='s')
    order_status        = models.CharField(max_length=2, choices=ORDER_STATUS,      default='w')
    is_sample           = models.BooleanField(default = False)

    created_at  = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()

    objects     = models.Manager() # The default manager.
    active      = ActiveChartManager() # The Active Charts
    samples     = ActiveSamplesManager() # The Active Samples

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super().save(*args, **kwargs)  

    def __str__(self):
        return self.session_id

    def total_price(self):
        total = 0
        if self.is_sample:
            return total

        for ch_i in self.chart_item.filter(status = 'ok'):
            total += ch_i.tot_quantity() * ch_i.product.price(ch_i.size)
        return total
    
    def all_samples(self):
        if self.chart_item and self.is_sample:
            return self.chart_item.filter(status = 'ok')
    
    def all_items(self):
        if self.chart_item and (not self.is_sample):
            return self.chart_item.filter(status = 'ok')

    def is_in_sample(self, product_code):
        if self.chart_item and self.is_sample:
            return self.chart_item.filter(status = 'ok',product__code = product_code)


class ChartItem(models.Model):
    chart       = models.ForeignKey(Chart,      verbose_name="Charts",      null=True, blank = True, on_delete=models.CASCADE, related_name='chart_item')
    product     = models.ForeignKey(Product,    verbose_name="Products",    null=True, blank = True, on_delete=models.CASCADE, related_name='chart_item')
    size        = models.ForeignKey(Tag,        verbose_name="Tags",        null=True, blank = True, on_delete=models.CASCADE, related_name='chart_item')
    quantity    = models.PositiveIntegerField( default=1 )       
    has_frido   = models.BooleanField(default = True)

    status      = models.CharField(choices = ITEM_STATUS, max_length=2,  default='ok')
    created_at  = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        if self.chart:
            return self.chart.session_id        
        else:
            return self.status

    def price(self):
        if self.status == 'ok':
            return compute_price(self.quantity, self.has_frido, self.product.price(self.size))

class Question(models.Model):
    content         = models.TextField()
    modified_at     = models.DateTimeField()    
    created_at      = models.DateTimeField("date created",editable=False)
    publish_date    = models.DateTimeField("date published", blank = True, null = True, auto_now_add=False)

    reply           = models.ForeignKey("self", blank = True, null = True,on_delete=models.SET_NULL, related_name='question' )
    public          = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super().save(*args, **kwargs)

    def published(self):
        return True #models.BooleanField(default = True)
  