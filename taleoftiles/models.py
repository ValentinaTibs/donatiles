from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models import Count

from taleoftiles.utils  import min_price,max_price

import datetime as dt
import pytz

DATA_TYPE = (
    ('t', 'Text'),
    ('b', 'Boolean'),
    ('c', 'Color'),
    ('i', 'Integer')
) 

class MenuTagManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().filter(
            in_menu = True, 
            public = True,)
        return qs

class CatalogueTagManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().filter(
            in_catalogue = True, 
            public = True,
            )
        return qs

class Tag(models.Model):
    name    = models.CharField(max_length=200)
    summary = models.CharField(max_length=200, null = True, blank=True,)
    slug    = models.CharField(max_length=200,  unique=True)
    public  = models.BooleanField(default = True)

    in_catalogue    = models.BooleanField(default = False)    
    in_menu         = models.BooleanField(default = False)    
    in_home         = models.BooleanField(default = False)    
    in_product_edit = models.BooleanField(default = False)    
    in_footer       = models.BooleanField(default = False)    
    parent      = models.ForeignKey("self", blank = True, null = True, on_delete=models.SET_NULL, related_name='child' )

    data_type   = models.CharField(max_length=2, choices=DATA_TYPE, default='t')
    order       = models.PositiveIntegerField(default = 0)
    
    objects     = models.Manager() # The default manager.
    catalogues   = CatalogueTagManager()
    
    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Tags"
        ordering = ["order","name"] 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.replace(" ","-").lower()
        super().save(*args, **kwargs)  # Call the "real" save() method.
    
    def __str__(self):
        return self.name

    def childs(self):
        return Tag.objects.filter(parent = self,public='True')

    def has_childs(self):
        return (Tag.objects.filter(parent = self).count > 0)

    def all_menu_childs(self):
        return Tag.objects.filter(parent = self,in_menu = True, public = True)

    def all_footer_childs(self):
        return Tag.objects.filter(parent = self,in_footer = True, public = True)

    def all_catalogue_childs(self):
        return Tag.objects.filter(parent = self,in_catalogue = True, public = True)


class Publication(models.Model):
    title   = models.CharField(max_length=200, unique = True)
    content = models.TextField()

    created_at  = models.DateTimeField(editable=False, blank=True,null=False )
    modified_at = models.DateTimeField(editable=False, blank=True,null=False)

    publish_date    = models.DateTimeField("date published", blank=True,null=False)
    slug            = models.CharField(max_length=200, unique=True, blank=True,null=False)
    author          = models.ForeignKey( User, on_delete=models.CASCADE, blank=True,null=False )
    
    def __str__(self):
        if self.title == "":
            return "-"
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.title.replace(" ","-").lower()

        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()

        if not self.publish_date:
            self.publish_date = timezone.now()

        return super().save(*args, **kwargs)  # Call the "real" save() method.
        

class TechnicalSpec(models.Model):
    slug    = models.CharField(max_length=50, unique=True)
    file    = models.FileField(upload_to='techspecs/')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.imagefile.name.replace(" ","-").lower()
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.slug

class ActiveProductManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().filter(
            publication__publish_date__lte= dt.datetime.now(), 
            is_active = True)
        return qs

# class TagsToProduct(models.Model):

#     product     = models.ForeignKey('Product',  related_name='ttp', on_delete=models.SET_NULL, null=True,blank= True)
#     tags        = models.ForeignKey('Tag',      related_name='tagsto_products', on_delete=models.SET_NULL, null=True, blank=True)
#     default     = models.BooleanField(default = False)

class Product(models.Model):
    
    name            = models.CharField(max_length=100,)
    wait_time       = models.PositiveIntegerField(default = 15)
    min_ammount     = models.PositiveIntegerField(default = 5)
    code            = models.CharField(max_length=100,unique=True,)
    is_decor        = models.BooleanField(default = False)
    available       = models.BooleanField(default = True)
    is_active       = models.BooleanField(default = True)
    
    tags            = models.ManyToManyField(Tag,  blank= True, related_name='products')
    
    publication     = models.ForeignKey(Publication, blank = True,  null = True,on_delete=models.CASCADE, related_name='products' )    
    support_to      = models.ForeignKey("self", blank = True, null = True,on_delete=models.SET_NULL, related_name='supports' )
    techspec        = models.ForeignKey(TechnicalSpec, blank = True, null = True, on_delete=models.SET_NULL, related_name='products' )
    order           = models.PositiveIntegerField(default = 0)

    MPN             = models.CharField(max_length=100, null = True, blank=True)
    
    objects     = models.Manager() # The default manager.
    active      = ActiveProductManager() # The Active Charts

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Products"
        ordering = ["order","name"]     

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.name.replace(" ","-").lower()
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return self.code

    def is_support(self,):
        return self.support_to.is_null == True

    def thumb_(self):
        for image in self.images.all():
            if image.is_cover:
                return image.thumb_()
    
    def cover(self):
        for image in self.images.all():
            if image.is_cover:
                return image
    
    def single_sell(self):
        return False

    def serie(self,):
        try:
            serie = self.tags.get(parent__slug = 'serie')
        except ObjectDoesNotExist:
            serie = "None"
        return serie

    def colour(self,):
        try:
            col = self.tags.filter(parent__slug = 'colour').first()
        except ObjectDoesNotExist:
            col = "None"
        return col    

    def is_samplable(self,):
        try:
            se = self.tags.get(slug = 'samplable')
        except ObjectDoesNotExist:
            return False    
        return True

    def get_tag(self,tag_slug):
        try:
            serie = self.tags.get(parent__slug = tag_slug)
        except ObjectDoesNotExist:
            serie = "None"
        return serie

    def filter_tags(self,tag_slug):
        res = self.tags.filter(parent__slug = tag_slug)
        if res.count() == 0:
            res= "none"
        return res

    def formats(self):
        res = self.tags.filter(parent__parent__slug = "format")
        if res.count() == 0:
            res= "none"
        return res
    
    def default_format(self):
        prices = self.prices.filter(default = True)
        if prices.count() == 0:
            return None
        return prices.first().size

    def price(self,size ):
        try: 
            price = self.prices.get(size__slug = size)
        except ObjectDoesNotExist:
            return 1
        return price.euros

    def m2_box(self,size ):
        
        try: 
            price = self.prices.get(size__slug = size)
        except ObjectDoesNotExist:
            return 1
        return price.m2_box
    
    def weight_box(self,size ):
        try: 
            price = self.prices.get(size__slug = size)
        except ObjectDoesNotExist:
            return 1
        return price.weight_box
    
    def compute_price(self, size = None):
        if self.single_sell:
            return compute_single_price(0,0,0,0)
        else:
            return compute_sm_price(self.quantity, self.has_frido, self.product.price(self.size),self.product.m2_box(self.size),self.weight_box(self.size))

    
    def min_price(self,format):
        return round(min_price(self.price(format), self.m2_box(format), self.weight_box(format)),2)

    def max_price(self,format):
        return round(max_price(self.price(format), self.m2_box(format), self.weight_box(format)),2)    
    


class EasyProductProxy(Product):

    class Meta:
        proxy = True
            
class Price(models.Model):
    size        = models.ForeignKey(Tag,     blank = True, null = True, on_delete=models.SET_NULL, related_name='prices')
    product     = models.ForeignKey(Product, blank = True, null = True, on_delete=models.SET_NULL, related_name='prices' )
    euros       = models.FloatField(default = 10)
    m2_box      = models.FloatField(default = 10)
    weight_box  = models.FloatField(default = 10)

    default     = models.BooleanField(default = False)

    def __str__(self):
        if self.size and self.size.name and self.product.publication and self.product.publication.title :
            return self.size.name + self.product.publication.title + str(self.euros)
        else:
            return str(self.euros)
    
class Catalogue(models.Model):
    title       = models.CharField(max_length=200, unique = True)
    active      = models.BooleanField(default = True)
    products    = models.ManyToManyField(Product, blank = True, null = True,  related_name='catalogues' ) 
    

    def tags(self):
        return Tag.objects.filter(in_catalogue = True,parent__isnull = True).in_bulk(field_name='slug')

    # def filter_products(self,prods,query_dictionary):
        
    #     tag_query = Q()
    #     tag_len = 0
    #     for key, value in query_dictionary.items():
    #         if(key != 'csrfmiddlewaretoken') and len(value[0]) >0:
    #             tag_query = tag_query | Q(slug = value[0])
    #             tag_len = tag_len + 1
        
    #     if tag_query == Q():
    #         return prods
    #     active_tags = Tag.objects.filter(tag_query)
    #     return prods.filter(tags__in=active_tags).annotate(num_tags=Count('tags')).filter(num_tags=tag_len).distinct()

    def __str__(self):
        return self.title
        
