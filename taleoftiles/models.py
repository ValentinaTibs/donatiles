from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

from PIL import Image

class Image(models.Model):  
    name =  models.CharField (max_length = 100 , null = True, blank=True)
    imagefile = models.ImageField( upload_to='photos', null=True, blank=True, help_text="Load an image.")

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

class Tag(models.Model):
    
    tag_name = models.CharField(max_length=200)
    tag_summary = models.CharField(max_length=200)
    tag_slug = models.CharField(max_length=200, default=1)
    public =models.BooleanField(default = True)

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.tag_name

class PostRelated(models.Model):
    post_related = models.CharField(max_length=200)
    post_tag = models.ForeignKey(Tag, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)
    summary = models.CharField(max_length=200)

    class Meta:
        # otherwise we get "Tutorial Seriess in admin"
        verbose_name_plural = "Related"

    def __str__(self):
        return self.post_related

class Post(models.Model):
    title = models.CharField(max_length=200, unique = True)
    content = models.TextField()
    create_date = models.DateTimeField("date created", auto_now_add=True)
    publish_date = models.DateTimeField("date published", auto_now_add=False)
    image = models.ForeignKey(Image, verbose_name="Image", on_delete=models.SET_NULL, null = True)

    related = models.ForeignKey(PostRelated, default=1, verbose_name="Post Related", on_delete=models.SET_DEFAULT)
    slug = models.CharField(max_length=200, unique=True)

    author = models.ForeignKey( User, on_delete=models.CASCADE )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.title.replace(" ","-").lower()
        super().save(*args, **kwargs)  # Call the "real" save() method.


# class Tag(models.Model):
#     name =   models.CharField (max_length = 100 , null = True, blank=True)
#     slug =   models.CharField (max_length = 100 , null = True, blank=True, unique = True)



# class Publication(models.Model):
#     create_date = models.DateTimeField("date created", auto_now_add=True)
#     publish_date = models.DateTimeField("date published", auto_now_add=False)
#     title = models.CharField(max_length=200)
#     text  = models.TextField ()
#     slug = models.SlugField()
#     #2do the nullable part of this code must change 
#     author = models.ForeignKey( User, on_delete=models.CASCADE )

#     def __str__(self):
#         return '%s' % (self.title,)

# class Related(models.Model):
#     rel_pub = models.ManyToManyField(Publication)


# class Post(models.Model):
#     pub = models.ForeignKey('Publication', on_delete=models.CASCADE)
#     rel = models.ForeignKey('Related', on_delete=models.CASCADE)

# class Product(models.Model): 
#     pub = models.ForeignKey('Publication', on_delete=models.CASCADE)
#     rel = models.ForeignKey('Related', on_delete=models.CASCADE)

# class ProductImage(models.Model): 
#     image = models.ForeignKey('Image', on_delete=models.SET_NULL, null = True)
#     product = models.ForeignKey('Product', on_delete=models.CASCADE)
    
     
    
# class Setting(models.Model):
#     posts = models.ForeignKey('Post', on_delete=models.CASCADE)
#     products = models.ForeignKey('Products', on_delete=models.SET_NULL)
    
