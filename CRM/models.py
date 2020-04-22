from django.utils.crypto import get_random_string

from django.db import models
from taleoftiles.models import Product
# Create your models here.

COMPLETION_STATUS = (
    ('e', 'Empty'),
    ('s', 'Started'),
    ('c', 'Completed'),
    ('o', 'Ordered'),
    ('ex', 'Expired')
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


class Chart(models.Model):
	session_id = models.CharField(max_length=100, unique=True, default="")
	completion_status = models.CharField(max_length=2, choices=COMPLETION_STATUS, default='e')
	order_status = models.CharField(max_length=2, choices=ORDER_STATUS, default='w')
	is_sample = models.BooleanField(default = False)

	def __str__(self):
		return self.session_id


class ChartItem(models.Model):
	chart = models.ForeignKey(Chart,  verbose_name="Charts", null=True, on_delete=models.SET_NULL, related_name='chart_item')
	product = models.ForeignKey(Product,  verbose_name="Products", null=True, on_delete=models.SET_NULL, related_name='chart_item')
	removed = models.BooleanField(default = False)

	quantity = models.PositiveIntegerField( default=1 )   

	def __str__(self):
		return self.Chart.session_id        


        
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

def create_shipping_internal_id():
	return get_random_string(length=32)

class Order(models.Model):
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
    note = models.TextField(max_length = 200, null = True)

    internal_tracking_id = models.CharField(max_length=100, default = "")
    shipping_tracking_id= models.CharField(max_length=100, default = "")

    chart = models.ForeignKey(Chart, verbose_name="Chart", null = False, on_delete=models.CASCADE, related_name='shipping')

    def save(self, *args, **kwargs):
        self.internal_tracking_id = create_shipping_internal_id

        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return self.internal_tracking_id

class Question(models.Model):
    content = models.TextField()
    # name    = models.CharField(max_length=100,default = "")
    # surname = models.CharField(max_length=100,default = "")

    # email   = models.EmailField(max_length=100,default = "")
    # telephone = models.CharField(max_length=100,default = "")
    published = models.BooleanField(default = True)

    create_date  = models.DateTimeField("date created", auto_now_add=True)
    publish_date = models.DateTimeField("date published", blank = True, null = True, auto_now_add=False)

    reply = models.ForeignKey("self", blank = True, null = True,on_delete=models.SET_NULL, related_name='question' )
    # user - that might be null 
    # author that might be a user - that might be null 
    # status visible only to the staff
    # creation date
    # email to reply

    # null=True, to allow in database
    # blank=True, to allow in form validation

# class Order(models.Model):
#     pass