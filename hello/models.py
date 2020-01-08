from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

from PIL import Image

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class Image(models.Model):  
    name =   models.CharField (max_length = 100 , null = True, blank=True)
    imagefile = models.ImageField( upload_to='photos', null=True, blank=True, help_text="Load an image.")

    def image_(self):
        return mark_safe('<img src="/media/{0}">'.format(self.imagefile))

    def thumb_(self):
        width = 30
        ratio = 30 / self.imagefile.width
        height = self.imagefile.height * ratio
        return mark_safe('<a href="/media/{0}"><img src="/media/{0}" width={1} height={2}></a>'.format(self.imagefile,width,height))

    def __str__(self):
        return '%s' % (self.imagefile,)

    def save(self, *args, **kwargs):
        if(self.name == None):
            self.name = self.imagefile.name
        super().save(*args, **kwargs)  # Call the "real" save() method.

class Post(models.Model):
    create_date = models.DateTimeField("date created", auto_now_add=True)
    publish_date = models.DateTimeField("date published", auto_now_add=False)
    title = models.CharField(max_length=200)
    text  = models.TextField ()
    slug = models.SlugField()
    #2do the nullable part of this code must change 
    images = models.ForeignKey('Image', on_delete=models.SET_NULL, null = True)
    author = models.ForeignKey( User, on_delete=models.CASCADE )

    def __str__(self):
        return '%s' % (self.title,)


# class Product(models.Model): 
#     images = models.ForeignKey('Image', on_delete=models.CASCADE)
#     name  = models.CharField ()

# class Setting(models.Model):
#     posts = models.ForeignKey('Post', on_delete=models.CASCADE)
#     products = models.ForeignKey('Products', on_delete=models.SET_NULL)
    
