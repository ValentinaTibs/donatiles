from django.utils.crypto import get_random_string

from django.db import models

from taleoftiles.models import Product
from django.utils import timezone


from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


#### ------- Move this to SIgnals.py
from django.contrib.auth.signals import user_logged_in

def pour_charts(sender, user, request, **kwargs):
    session_loc_id = request.session.session_key

    for chart in Chart.objects.filter( session_id  = session_loc_id): 
        chart.user = user
        chart.save()

user_logged_in.connect(pour_charts)

#####  --------------


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = False)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()


class Shipping(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = False)
    fullname = models.TextField(max_length=100, blank=True)
    #2do this must be a selectebox...for now is a text field
    #country = models.CharField(max_length=2, choices=COMPLETION_STATUS, default='s')
    country = models.TextField(max_length=100, blank=True)
    city = models.TextField(max_length=100, blank=True)
    CAP = models.TextField(max_length=10, blank=True)
    shipping_address = models.TextField(max_length=100, blank=True)
    telephone_num = models.TextField(max_length=30, blank=True)


COMPLETION_STATUS = (
    ('s', 'Started'),
    ('c', 'Completed'),
    ('o', 'Ordered'),
    ('ex', 'Expired'),
    ('cs', 'Closed by Staff'),
) 

ORDER_STATUS = (
    ('w', 'In Wait'),
    ('i', 'Received'),
    ('p', 'In Preparazione'),
    ('s', 'Spedito'),
    ('l', 'Lost'),
    ('r', 'Ricevuto'),
    ('c', 'Confermato'),
) 

ITEM_STATUS = (
    ('ok', 'ok'),
    ('ns', 'Not Samplable'),
    ('le', 'Limit Exceeded'),
    ('ru', 'Removed by User'),
    ('rs', 'Removed by Staff'),
    ('o', 'Others')
) 

class Chart(models.Model):
    session_id  = models.CharField(max_length=100, default="", null = True)
    user        = models.ForeignKey( User,  blank = True, null = True, on_delete=models.SET_NULL, related_name='orders' )

    completion_status   = models.CharField(max_length=2, choices=COMPLETION_STATUS, default='s')
    order_status        = models.CharField(max_length=2, choices=ORDER_STATUS, default='w')
    is_sample           = models.BooleanField(default = False)

    created_at  = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super().save(*args, **kwargs)  

    def __str__(self):
        return self.session_id

    def num_prods(self):
        if self.chart_item:
            return self.chart_item.filter(status = 'ok').count()
        else:
            return 0

    def all_samples(self):
        if self.chart_item and self.is_sample:
            return self.chart_item.filter(status = 'ok')
    
    def all_items(self):
        if self.chart_item and (not self.is_sample):
            return self.chart_item.filter(status = 'ok')

class ChartItem(models.Model):
    chart       = models.ForeignKey(Chart,  verbose_name="Charts", null=True, on_delete=models.SET_NULL, related_name='chart_item')
    product     = models.ForeignKey(Product,  verbose_name="Products", null=True, on_delete=models.SET_NULL, related_name='chart_item')
    status     = models.CharField(max_length=2, choices=ITEM_STATUS, default='ok')

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
   

def create_shipping_internal_id():
    return get_random_string(length=32)

class Order(models.Model):
    note = models.TextField(max_length = 200, null = True)

    internal_tracking_id = models.CharField(max_length=100, default = "")
    shipping_tracking_id= models.CharField(max_length=100, default = "")

    chart = models.ForeignKey(Chart, verbose_name="Chart", null = False, on_delete=models.CASCADE, related_name='shipping')

    def save(self, *args, **kwargs):
        self.internal_tracking_id = create_shipping_internal_id

        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return self.internal_tracking_id
    #user = models.ForeignKey(User,  verbose_name="User", null=True, on_delete=models.SET_NULL)
    #completion_status = models.CharField(max_length=2, choices=COMPLETION_STATUS, default='e')
    # name    = models.CharField(max_length=100,default = "")
    # surname = models.CharField(max_length=100,default = "")
    
    # email   = models.EmailField(max_length=100,default = "")
    # telephone = models.CharField(max_length=100,default = "")

    # address = models.CharField(max_length=100,default = "")
    # address2 = models.CharField(max_length=100,default = "")
    # city = models.CharField(max_length=100,default = "")
    # postcode = models.CharField(max_length=100,default = "")
    

class Question(models.Model):
    content = models.TextField()
    # name    = models.CharField(max_length=100,default = "")
    # surname = models.CharField(max_length=100,default = "")

    # email   = models.EmailField(max_length=100,default = "")
    # telephone = models.CharField(max_length=100,default = "")

    modified_at = models.DateTimeField()    
    created_at  = models.DateTimeField("date created",editable=False)
    publish_date = models.DateTimeField("date published", blank = True, null = True, auto_now_add=False)

    reply = models.ForeignKey("self", blank = True, null = True,on_delete=models.SET_NULL, related_name='question' )

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super().save(*args, **kwargs)

    def published(self):
        return True #models.BooleanField(default = True)

    # user - that might be null 
    # author that might be a user - that might be null 
    # status visible only to the staff
    # creation date
    # email to reply

    # null=True, to allow in database
    # blank=True, to allow in form validation

    # class Order(models.Model):
    #     pass




        
# class Sample(models.Model):
#     session_id = models.CharField(max_length=100, unique=True, default="")
#     completion_status = models.CharField(max_length=2, choices=COMPLETION_STATUS, default='e')
#     order_status = models.CharField(max_length=2, choices=ORDER_STATUS, default='w')

#     def __str__(self):
#         return self.session_id

# class SampleItem(models.Model):
#     product = models.ForeignKey(Product,  verbose_name="Products", null=True, on_delete=models.SET_NULL, related_name='sample')
#     sampler = models.ForeignKey(Sample,  verbose_name="Sampler", null=True, on_delete=models.SET_NULL, related_name='sample')
#     removed = models.BooleanField(default = False)

#     def __str__(self):
#         return self.sampler.session_id     