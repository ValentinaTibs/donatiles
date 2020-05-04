from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models import Count


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
        return mark_safe('<img src="/icons/{0}">'.format(self.imagefile))

    def __str__(self):
        return '%s' % (self.name, )

class Tag(models.Model):
    name    = models.CharField(max_length=200)
    summary = models.CharField(max_length=200, null = True, blank=True,)
    slug    = models.CharField(max_length=200,  unique=True)
    public  = models.BooleanField(default = True)

    in_catalogue= models.BooleanField(default = False)    
    in_menu     = models.BooleanField(default = False)    
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
    title = models.CharField(max_length=200, unique = True)
    content = models.TextField()

    created_at  = models.DateTimeField(editable=False, blank=True,null=False )
    modified_at = models.DateTimeField(editable=False, blank=True,null=False)

    publish_date = models.DateTimeField("date published", blank=True,null=False)
    slug = models.CharField(max_length=200, unique=True, blank=True,null=False)
    author = models.ForeignKey( User, on_delete=models.CASCADE, blank=True,null=False )
    
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
    slug = models.CharField(max_length=50, unique=True)
    icons = models.ManyToManyField(Icon,  blank= True, related_name='techspecs')
    file =  models.FileField(upload_to='techspecs/')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.imagefile.name.replace(" ","-").lower()
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.slug


class Product(models.Model):
    price = models.PositiveIntegerField( default=0, )
    
    wait_time = models.PositiveIntegerField(default = 15)
    min_ammount = models.PositiveIntegerField(default = 5)
    code = models.CharField(max_length=100,)
    
    tags = models.ManyToManyField(Tag, blank= True, related_name='products')
    publication = models.OneToOneField(Publication, blank = True,  null = True,on_delete=models.CASCADE, related_name='products' )
    techspec = models.ForeignKey(TechnicalSpec, blank = True, null = True, on_delete=models.SET_NULL, related_name='products' )

    support_to = models.ForeignKey("self", blank = True, null = True,on_delete=models.SET_NULL, related_name='supports' )
    is_decor = models.BooleanField(default = False)
    is_samplable = models.BooleanField ( default=True, null = True)
    available  = models.BooleanField(default = True)
    active = models.BooleanField(default = False)

    # single_sell = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.name.replace(" ","-").lower()
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return self.publication.title

    def is_support(self,):
        return self.support_to.is_null == True
    
    def has_single_sell(self):
        return true

    def serie(self):
        try:
            serie = self.tags.get(parent__slug = "serie")
        except ObjectDoesNotExist:
            serie = "None"
        return serie

    def color(self):
        try:
            color = self.tags.get(parent__slug = "colour")
        except ObjectDoesNotExist:
            color = "FFFFFF"
        return color

    def formats(self):    
        formats = self.tags.filter(parent__slug = "format")
        if formats.count() == 0:
            formats= "none"
        return formats

    def finishes(self):    
        finishes = self.tags.filter(parent__slug = "finish")
        if finishes.count() == 0:
            finishes= "none"        
        return finishes

class Catalogue(models.Model):
    title = models.CharField(max_length=200, unique = True)
    active = models.BooleanField(default = True)

    # def catalogue_childs(self):
    #     return Tag.objects.filter(parent = self, in_catalogue = True)

    def tags(self):
        return Tag.objects.filter(in_catalogue = True,parent__isnull = True).in_bulk(field_name='slug')

    def filter_products(self,prods,query_dictionary):
        
        tag_query = Q()
        tag_len = 0
        for key, value in query_dictionary:
            if(key != 'csrfmiddlewaretoken'):
                tag_query = tag_query | Q(slug = value)
                tag_len = tag_len + 1

        active_tags = Tag.objects.filter(tag_query)
        
        return prods.filter(tags__in=active_tags).annotate(num_tags=Count('tags')).filter(num_tags=tag_len).distinct()
        

class Photo(models.Model):  

    name =  models.CharField (max_length = 100 , null = True, blank=True)
    imagefile = models.ImageField( upload_to='photos', null=True, blank=True, help_text="Load an image.")
    # collection = models.ForeignKey(Collection,blank = True,  null = True,on_delete=models.SET_NULL, related_name='images' )
    product = models.ForeignKey(Product, blank = True, null = True,on_delete=models.SET_NULL, related_name='images' )
    # setting = models.ForeignKey(Setting, blank = True, null = True,on_delete=models.SET_NULL, related_name='images' )
    # post = models.ForeignKey(Post, blank = True, null = True,on_delete=models.SET_NULL, related_name='images' )
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


#from PIL import Image



# class TecnicalSpec(models.Model):
#     note = models.TextField(max_length = 200, null = True)

# class Format(models.Model):
#     title = models.CharField(max_length=100, default="10x10")
#     description = models.CharField(max_length=100, null=True)
#     slug = models.CharField(max_length=50, unique=True)

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = self.title.replace(" ","-").lower()
#         super().save(*args, **kwargs)  

#     def __str__(self):
#         return self.title

# class Collection(models.Model):
#     specs = models.ForeignKey(TecnicalSpec, blank = True, null = True, on_delete=models.SET_NULL, related_name='collection' )
#     formats = models.ManyToManyField(Format,  blank= True, related_name='collection')

#     def __str__(self):
#         return self.publication.title

# class Color(models.Model):
#     title = models.CharField(max_length=100, default="white")
#     description = models.CharField(max_length=100, null=True)
#     slug = models.CharField(max_length=50, unique=True)

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = self.title.replace(" ","-").lower()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.title
  

# class Finish(models.Model):
#     title = models.CharField(max_length=100, default="matte")
#     description = models.CharField(max_length=100, null=True)
#     slug = models.CharField(max_length=50, unique=True)
    
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = self.title.replace(" ","-").lower()
#         super().save(*args, **kwargs)  

#     def __str__(self):
#         return self.title

# class Setting(models.Model):
#     products = models.ManyToManyField(Product, blank= True, related_name='settings')

#     def __str__(self):
#         return self.publication.title

#     #pub = models.OneToOneField(Publication, on_delete=models.CASCADE, related_name='post' )

# class Profile(models.Model):
#     user = models.OneToOneField( User, related_name="profile", on_delete=models.CASCADE,verbose_name="user")

#     # Attributes - Mandatory
#     interaction = models.PositiveIntegerField( default=0, )

#      # Custom Properties
#     @property
#     def username(self):
#         return self.user.username
  
#     def __str__(self):
#         return self.user.username



#     