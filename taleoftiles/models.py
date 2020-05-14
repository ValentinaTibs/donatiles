from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models import Count

import datetime as dt


DATA_TYPE = (
    ('t', 'Text'),
    ('b', 'Boolean'),
    ('c', 'Color'),
    ('i', 'Integer')
) 

class Icon(models.Model):  
    name        =  models.CharField (max_length = 100 , null = False, blank=False, unique=True)
    imagefile   = models.ImageField( upload_to='icons', null=True, blank=True, help_text="Load an image.", unique=True)
    description = models.TextField()

    def image_(self):
        return mark_safe('<img src="/media/{0}">'.format(self.imagefile))

    def __str__(self):
        return '%s' % (self.name, )

class Tag(models.Model):
    name    = models.CharField(max_length=200)
    summary = models.CharField(max_length=200, null = True, blank=True,)
    slug    = models.CharField(max_length=200,  unique=True)
    public  = models.BooleanField(default = True)

    in_catalogue    = models.BooleanField(default = False)    
    in_menu         = models.BooleanField(default = False)    
    in_home         = models.BooleanField(default = False)    
    in_product_edit = models.BooleanField(default = False)    
    icon        = models.ForeignKey( Icon,  blank = True, null = True, on_delete=models.SET_NULL, related_name='tags' )
    parent      = models.ForeignKey("self", blank = True, null = True, on_delete=models.SET_NULL, related_name='child' )

    data_type   = models.CharField(max_length=2, choices=DATA_TYPE, default='t')
    order       = models.PositiveIntegerField(default = 0)

    #catalogue = models.ForeignKey(Catalogue, blank= True, null = True,on_delete=models.SET_NULL,related_name='all_tags' )
    
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

    def childs(self):
        return Tag.objects.filter(parent = self)

    def has_childs(self):
        return (Tag.objects.filter(parent = self).count > 0)


class Publication(models.Model):
    title   = models.CharField(max_length=200, unique = True)
    content = models.TextField()

    created_at  = models.DateTimeField(editable=False, blank=True,null=False )
    modified_at = models.DateTimeField(editable=False, blank=True,null=False)

    publish_date    = models.DateTimeField("date published", blank=True,null=False)
    slug            = models.CharField(max_length=200, unique=True, blank=True,null=False)
    author          = models.ForeignKey( User, on_delete=models.CASCADE, blank=True,null=False )
    
    def __str__(self):
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
    icons   = models.ManyToManyField(Icon,  blank= True, related_name='techspecs')
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

class Product(models.Model):
    
    wait_time       = models.PositiveIntegerField(default = 15)
    min_ammount     = models.PositiveIntegerField(default = 5)
    code            = models.CharField(max_length=100,unique=True,)
    is_decor        = models.BooleanField(default = False)
    is_samplable    = models.BooleanField( default=True, null = True)
    available       = models.BooleanField(default = True)
    is_active       = models.BooleanField(default = True)
    tags            = models.ManyToManyField(Tag, blank= True, related_name='products')
    publication     = models.ForeignKey(Publication, blank = True,  null = True,on_delete=models.CASCADE, related_name='products' )
    support_to      = models.ForeignKey("self", blank = True, null = True,on_delete=models.SET_NULL, related_name='supports' )
    techspec        = models.ForeignKey(TechnicalSpec, blank = True, null = True, on_delete=models.SET_NULL, related_name='products' )

    objects     = models.Manager() # The default manager.
    active      = ActiveProductManager() # The Active Charts

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
    
    def has_single_sell(self):
        return true

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

class Price(models.Model):
    size    = models.ForeignKey(Tag,     blank = True, null = True, on_delete=models.SET_NULL, related_name='prices')
    product = models.ForeignKey(Product, blank = True, null = True, on_delete=models.SET_NULL, related_name='prices' )
    euros   = models.PositiveIntegerField(default = 10)

    def __str__(self):
        return self.size.name + self.product.publication.title + str(self.euros)
    
class Catalogue(models.Model):
    title = models.CharField(max_length=200, unique = True)
    active = models.BooleanField(default = True)

    def tags(self):
        return Tag.objects.filter(in_catalogue = True,parent__isnull = True).in_bulk(field_name='slug')

    def filter_products(self,prods,query_dictionary):
        
        tag_query = Q()
        tag_len = 0
        for key, value in query_dictionary.items():
            if(key != 'csrfmiddlewaretoken') and len(value[0]) >0:
                tag_query = tag_query | Q(slug = value[0])
                tag_len = tag_len + 1
        
        if tag_query == Q():
            return prods
        active_tags = Tag.objects.filter(tag_query)
        return prods.filter(tags__in=active_tags).annotate(num_tags=Count('tags')).filter(num_tags=tag_len).distinct()

    def __str__(self):
        return self.title
        

class Photo(models.Model):  

    name        = models.CharField (max_length = 100 , null = True, blank=True)
    imagefile   = models.ImageField( upload_to='photos', null=True, blank=True, help_text="Load an image.")
    product     = models.ForeignKey(Product, blank = True, null = True,on_delete=models.SET_NULL, related_name='images' )
    order       = models.PositiveIntegerField( default=0, )   
    is_cover    = models.BooleanField(default = False)

    class Meta:
        ordering = ["order"]    

    def image_(self):
        if self.imagefile:
            return mark_safe('<img src="/media/{0}">'.format(self.imagefile))
        else:
            return mark_safe('<img src="/media/photos/{0}">'.format(self.name))

    def thumb_(self):
        width = 30
        ratio = 30 / self.imagefile.width
        height = self.imagefile.height * ratio
        if self.imagefile:
            return mark_safe('<a href="/media/{0}"><img src="/media/{0}" width={1} height={2}></a>'.format(self.imagefile,width,height))
        else:
            return mark_safe('<a href="/media/photos/{0}"><img src="/media/photos/{0}" width={1} height={2}></a>'.format(self.name,width,height))

    def __str__(self):
        return '%s' % (self.name,)

    def save(self, *args, **kwargs):
        if(self.name == None):
            self.name = self.imagefile.name
        super().save(*args, **kwargs)  # Call the "real" save() method.

