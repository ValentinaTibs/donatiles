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
from taleoftiles.utils  import compute_single_price, compute_sm_price, compute_num_boxes

#### ------- Move this to SIgnals.py
from django.contrib.auth.signals import user_logged_in

def pour_charts_and_samplers(sender, user, request, **kwargs):
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
    
    for sampler in Sampler.active.filter( user = user): 
        sampler.session_id = session_loc_id
        sampler.save()

    for sampler in Sampler.objects.filter( session_id  = session_loc_id): 
        sampler.user = user
        sampler.save()

user_logged_in.connect(pour_charts_and_samplers)

#####  --------------
        
                

class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, null = False,related_name='profile')
    bio         = models.TextField(max_length=500, blank=True)
    location    = models.CharField(max_length=30, blank=True)
    birth_date  = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username       

    def name(self):
        if self.shipping:
            return self.shipping.fullname
        else:
            self.user.email
    
    def orders(self):
        query = Q(sampler__isnull = False, sampler__user = self.user) | Q(charts__isnull = False,charts__user = self.user) 
        return Order.objects.filter(query, )    

class Shipping(models.Model):
    #2do this must become a one to Many because we want to keep track of old shippings
    user                = models.OneToOneField(Profile, on_delete=models.SET_NULL, null = True)
    email               = models.TextField(max_length=100, blank=False)
    fullname            = models.TextField(max_length=100, blank=False)
    country             = models.CharField(max_length=2, choices=COUNTRY_LIST, default='it')
    city                = models.TextField(max_length=100, blank=False)
    CAP                 = models.TextField(max_length=10, blank=False)
    shipping_address    = models.TextField(max_length=100, blank=False)
    telephone_num       = models.TextField(max_length=30, blank=False)
    is_active           = models.BooleanField(default = True)



#2do mettere qui un metodo più decente
def create_shipping_internal_id():
    return get_random_string(length=12)

class Order(models.Model):

    note        = models.TextField(max_length = 200, null = True, blank=True)
    
    internal_tracking_id    = models.CharField(max_length=100, default = "")
    shipping_tracking_id    = models.CharField(max_length=100, default = "", blank=True)
    created_at              = models.DateTimeField(editable=False)
    modified_at             = models.DateTimeField()
    order_status            = models.CharField(max_length=2, choices=ORDER_STATUS, default='w')
    final_payment           = models.PositiveIntegerField( default=0 )   
    is_sampler              = models.BooleanField(default = False)
    shipping_date           = models.DateTimeField(editable=True,null= True, blank=True)
    
    #shipping                = models.ForeignKey(Shipping, null= True,on_delete=models.SET_NULL)
    
    def save(self, *args, **kwargs):
        if not self.internal_tracking_id:
            self.internal_tracking_id = create_shipping_internal_id()
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        
        super().save(*args, **kwargs)  # Call the "real" save() method.
    
    def __str__(self):
        return self.internal_tracking_id

   
    def user(self):
        if self.is_sampler:
            chart_model = self.sampler.first()
        else :
            chart_model = self.charts.first()
        if chart_model.user:
            return chart_model.user
        else :
            return None
    
    def total(self):
        total = 0
        for sample in self.sampler.all():
            total += sample.total_price()
        
        for chart in self.charts.all():
            total += chart.total_price()
        return total
    
    def is_paid(self):
        if self.is_sampler:
            for sampler in self.sampler.all():
                if not sampler.is_paid():
                    return False
        else:
            for chart in self.charts.all():
                if not chart.is_paid():
                    return False
        return True    
    
    def wait_time(self):
        if self.is_sampler:
            return 5
        else:
            my_max = 0
            for chart in self.charts.all():
                for chart_item in chart.chart_item.all():
                    my_max = max(my_max,chart_item.product.wait_time)
            return my_max
    

class ActiveChartManager(models.Manager):
    def get_queryset(self):
        query = Q(completion_status = 's') | Q(completion_status = 'i1') | Q(completion_status = 'i2') 
        qs = super().get_queryset().filter(query).annotate(
            ch_i_total = Count('chart_item',filter=Q(chart_item__status='ok')),
            ch_i_count = Sum('chart_item',filter=Q(chart_item__status='ok'))
        ).filter(ch_i_count__gt = 0)
        return qs


class Chart(models.Model):

    session_id  = models.CharField ( max_length=100, default="", null = True)
    user        = models.ForeignKey( User,  blank = True, null = True, on_delete=models.SET_NULL, related_name='charts' )
    order       = models.ForeignKey( Order, verbose_name="Order", null = True, on_delete=models.SET_NULL, related_name='charts')
    
    #2do probabilmente togliere questo da qui
    completion_status   = models.CharField(max_length=2, choices=COMPLETION_STATUS, default='s')
    
    created_at  = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()

    objects     = models.Manager() # The default manager.
    active      = ActiveChartManager() # The Active Charts
    
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
        
        for chart_item in self.chart_item.all():
            total += chart_item.price()
        return total
        
    def all_items(self):
        if self.chart_item:
            return self.chart_item.filter(status = 'ok')
    
    def is_paid(self):
        stat = self.completion_status
        if stat == 'p':
            return True
        return False

class ChartItem(models.Model):
    chart       = models.ForeignKey(Chart,      verbose_name="Charts",      null=True, blank = True, on_delete=models.CASCADE, related_name='chart_item')
    product     = models.ForeignKey(Product,    verbose_name="Products",    null=True, blank = True, on_delete=models.CASCADE, related_name='chart_item')
    size        = models.ForeignKey(Tag,        verbose_name="Tags",        null=True, blank = True, on_delete=models.CASCADE, related_name='chart_item')
    quantity    = models.PositiveIntegerField( default=1 )       
    #saved_price = models.PositiveIntegerField( )       
    has_frido   = models.BooleanField(default = True)

    boxes       = models.PositiveIntegerField( default=1,null=True, blank = True, )       
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
        if self.product.single_sell():
            return compute_single_price(0,0,0,0)
        else:
            return compute_sm_price(self.quantity, self.has_frido, self.product.price(self.size),self.product.m2_box(self.size),self.product.weight_box(self.size))

    def compute_num_boxes(self):
        return compute_num_boxes(self.quantity, self.has_frido, self.product.price(self.size),self.product.m2_box(self.size),self.product.weight_box(self.size))


    def tot_quantity(self):
        return 1

# return all charts that are samples and have at least one item 
class ActiveSamplesManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().filter(completion_status = 's').annotate(
            samples_total = Count('samples',filter=Q(samples__status='ok')),
            samples_count = Sum  ('samples',filter=Q(samples__status='ok'))
            ).filter(samples_count__gt = 0)
        return qs

class Sampler(models.Model):
    session_id  = models.CharField ( max_length=100, default="", null = True)
    user        = models.ForeignKey( User,  blank = True, null = True, on_delete=models.SET_NULL, related_name='samplers' )
    order       = models.ForeignKey( Order, verbose_name="Order", null = True, on_delete=models.SET_NULL, related_name='sampler')
    
    completion_status   = models.CharField(max_length=2, choices=COMPLETION_STATUS, default='s')
    
    created_at  = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()
    objects     = models.Manager() # The default manager.
    active      = ActiveSamplesManager() # The Active Charts
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super().save(*args, **kwargs)  

    def __str__(self):
        return self.session_id

    def total_price(self):
        total = 25
        
        #2do da riflettere meglio su questa condizione
        finalised_charts = Chart.objects.filter(user = self.user, completion_status='p')  
        paid_samples = Sampler.objects.filter(user = self.user, completion_status='p') 

        if finalised_charts.count() >= paid_samples.count()   :
            return 0
        return total
    
    def all_samples(self):
        return self.samples.filter(status = 'ok')
    
    def is_in_sample(self, product_code):
        if self.samples:
            return self.samples.filter(status = 'ok',product__code = product_code)

    def is_paid(self):
        stat = self.completion_status
        if stat == 'p':
            return True
        return False

class Sample(models.Model):
    sampler     = models.ForeignKey(Sampler, verbose_name="Samples", null=True, blank = True, on_delete=models.CASCADE, related_name='samples')
    product     = models.ForeignKey(Product,verbose_name="Products",null=True, blank = True, on_delete=models.CASCADE, related_name='samples')
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
        return self.sampler.session_id 

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
  