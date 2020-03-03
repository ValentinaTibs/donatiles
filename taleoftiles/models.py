from django.utils.safestring import mark_safe
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError


from django.contrib.auth.models import User
from django.db import models


from PIL import Image

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

class Tag(models.Model):
    name = models.CharField(max_length=200)
    summary = models.CharField(max_length=200, null = True, blank=True,)
    slug = models.CharField(max_length=200,  unique=True)
    public = models.BooleanField(default = True)
    in_menu = models.BooleanField(default = False)
    order = models.PositiveIntegerField(default = 0)

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Tags"
        ordering = ["order"] 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.replace(" ","-").lower()
        super().save(*args, **kwargs)  # Call the "real" save() method.
    
    def __str__(self):
        return self.name

class TecnicalSpec(models.Model):
    note = models.TextField(max_length = 200, null = True)

class Format(models.Model):
    title = models.CharField(max_length=100, default="10x10")
    description = models.CharField(max_length=100, null=True)
    slug = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.title.replace(" ","-").lower()
        super().save(*args, **kwargs)  

    def __str__(self):
        return self.title

class Collection(models.Model):
    specs = models.ForeignKey(TecnicalSpec, blank = True, null = True, on_delete=models.SET_NULL, related_name='collection' )
    formats = models.ManyToManyField(Format,  blank= True, related_name='collection')


    def __str__(self):
        return self.publication.title

class Color(models.Model):
    title = models.CharField(max_length=100, default="white")
    description = models.CharField(max_length=100, null=True)
    slug = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.title.replace(" ","-").lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
  

class Finish(models.Model):
    title = models.CharField(max_length=100, default="matte")
    description = models.CharField(max_length=100, null=True)
    slug = models.CharField(max_length=50, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.title.replace(" ","-").lower()
        super().save(*args, **kwargs)  

    def __str__(self):
        return self.title

class Product(models.Model):
    price = models.PositiveIntegerField( default=0, )
    samplable = models.BooleanField ( default=True, )
    wait_time = models.PositiveIntegerField(default = 15)
    min_ammount = models.PositiveIntegerField(default = 5)
    source = models.CharField(max_length=100, default="Italy")
    available  = models.BooleanField(default = True)

    collection = models.ForeignKey(Collection, null=True, blank= True, on_delete=models.SET_NULL, related_name='products')
    
    color = models.ForeignKey(Color, null=False, blank= False, on_delete=models.CASCADE, related_name='product')
    finish = models.ForeignKey(Finish, null=True, blank= True, on_delete=models.SET_NULL, related_name='product')

    is_decor = models.BooleanField(default = False)
    single_sell = models.BooleanField(default = False)

    # def save(self, *args, **kwargs):
    #     if not self.internal_name:
    #         self.internal_name = self.name.replace(" ","-").lower()
    #     super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return self.publication.title

class Setting(models.Model):
    products = models.ManyToManyField(Product, blank= True, related_name='settings')

    def __str__(self):
        return self.publication.title

class Post(models.Model):
    
    def __str__(self):
        return self.publication.title

    #pub = models.OneToOneField(Publication, on_delete=models.CASCADE, related_name='post' )

class Profile(models.Model):
    user = models.OneToOneField( User, related_name="profile", on_delete=models.CASCADE,verbose_name="user")

    # Attributes - Mandatory
    interaction = models.PositiveIntegerField( default=0, )

     # Custom Properties
    @property
    def username(self):
        return self.user.username
  
    def __str__(self):
        return self.user.username
        
class Sampler(models.Model):
    session_id = models.CharField(max_length=100, unique=True, default="")
    completion_status = models.CharField(max_length=2, choices=COMPLETION_STATUS, default='e')
    order_status = models.CharField(max_length=2, choices=ORDER_STATUS, default='w')


    def __str__(self):
        return self.session_id

class Sample(models.Model):
    product = models.ForeignKey(Product,  verbose_name="Products", null=True, on_delete=models.SET_NULL, related_name='sample')
    sampler = models.ForeignKey(Sampler,  verbose_name="Sampler", null=True, on_delete=models.SET_NULL, related_name='sample')
    removed = models.BooleanField(default = False)

    def __str__(self):
        return self.sampler.session_id        

class Chart(models.Model):
    session_id = models.CharField(max_length=100, unique=True, default="")
    completion_status = models.CharField(max_length=2, choices=COMPLETION_STATUS, default='e')
    order_status = models.CharField(max_length=2, choices=ORDER_STATUS, default='w')

class ChartItem(models.Model):
    product = models.ForeignKey(Product,  verbose_name="Products", null=True, on_delete=models.SET_NULL, related_name='chart_item')
    removed = models.BooleanField(default = False)
    chart = models.ForeignKey(Chart,  verbose_name="Charts", null=True, on_delete=models.SET_NULL, related_name='chart_item')
    
    squared_meter = models.PositiveIntegerField( default=1 )   

class Shipping(models.Model):
    #user = models.ForeignKey(User,  verbose_name="User", null=True, on_delete=models.SET_NULL)
    completion_status = models.CharField(max_length=2, choices=COMPLETION_STATUS, default='e')
    name    = models.CharField(max_length=100,default = "")
    surname = models.CharField(max_length=100,default = "")
    
    email   = models.EmailField(max_length=100,default = "")
    telephone = models.CharField(max_length=100,default = "")

    address = models.CharField(max_length=100,default = "")
    address2 = models.CharField(max_length=100,default = "")
    city = models.CharField(max_length=100,default = "")
    postcode = models.CharField(max_length=100,default = "")
    note = models.TextField(max_length = 200, null = True)

    internal_tracking_id = models.CharField(max_length=100, default = "")
    external_tracking_id= models.CharField(max_length=100, default = "")

    sampler = models.ForeignKey(Sampler,  verbose_name="Sampler", null = True, on_delete=models.CASCADE, related_name='shipping')
    chart = models.ForeignKey(Chart,  verbose_name="Chart",  null = True,on_delete=models.CASCADE, related_name='chart')

    def save(self, *args, **kwargs):
        self.internal_tracking_id = get_random_string(length=32)

        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return self.internal_tracking_id

class Order(models.Model):
    pass

class Question(models.Model):
    content = models.TextField()
    name    = models.CharField(max_length=100,default = "")
    surname = models.CharField(max_length=100,default = "")

    email   = models.EmailField(max_length=100,default = "")
    telephone = models.CharField(max_length=100,default = "")
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

class Publication(models.Model):
    title = models.CharField(max_length=200, unique = True)
    content = models.TextField()
    create_date = models.DateTimeField("date created", auto_now_add=True)
    publish_date = models.DateTimeField("date published", auto_now_add=False)
    tag = models.ManyToManyField(Tag,blank = True, verbose_name="Category", related_name='publication' )
    slug = models.CharField(max_length=200, unique=True)
    #author = models.ForeignKey( User,blank = True, on_delete=models.CASCADE )
    collection = models.OneToOneField(Collection,blank = True,  null = True,on_delete=models.CASCADE, related_name='publication' )
    product = models.OneToOneField(Product, blank = True, null = True,on_delete=models.CASCADE, related_name='publication' )
    setting = models.OneToOneField(Setting, blank = True, null = True,on_delete=models.CASCADE, related_name='publication' )
    post = models.OneToOneField(Post, blank = True, null = True,on_delete=models.CASCADE, related_name='publication' )
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.title.replace(" ","-").lower()
        #author = request.user
        super().save(*args, **kwargs)  # Call the "real" save() method.
  

class Image(models.Model):  

    name =  models.CharField (max_length = 100 , null = True, blank=True)
    imagefile = models.ImageField( upload_to='photos', null=True, blank=True, help_text="Load an image.")
    collection = models.ForeignKey(Collection,blank = True,  null = True,on_delete=models.SET_NULL, related_name='images' )
    product = models.ForeignKey(Product, blank = True, null = True,on_delete=models.SET_NULL, related_name='images' )
    setting = models.ForeignKey(Setting, blank = True, null = True,on_delete=models.SET_NULL, related_name='images' )
    post = models.ForeignKey(Post, blank = True, null = True,on_delete=models.SET_NULL, related_name='images' )
    order = models.PositiveIntegerField( default=0, )   

    class Meta:
        ordering = ["order"]    

    def image_(self):
        return mark_safe('<img src="/media/{0}">'.format(self.imagefile))

    def thumb_(self):
        width = 30
        ratio = 30 / self.imagefile.width
        height = self.imagefile.height * ratio
        return mark_safe('<a href="/media/{0}"><img src="/media/{0}" width={1} height={2}></a>'.format(self.imagefile,width,height))

    def __str__(self):
        return '%s' % (self.name,)

    def save(self, *args, **kwargs):
        if(self.name == None):
            self.name = self.imagefile.name
        super().save(*args, **kwargs)  # Call the "real" save() method.

class Config(models.Model):
    
    int_val= models.PositiveIntegerField( default=1,  null = True, blank=True) 
    char_val= models.CharField(max_length=100, default=1,  null = True, blank=True) 
    active = models.BooleanField(default = True)
    tag = models.CharField(max_length=20, default="-")

    def __str__(self):
        return '%s' % (self.tag,)
    