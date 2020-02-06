from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.db import models

from PIL import Image

class Tag(models.Model):
    name = models.CharField(max_length=200)
    summary = models.CharField(max_length=200, null = True, blank=True,)
    slug = models.CharField(max_length=200, default=1)
    public = models.BooleanField(default = True)
    in_menu = models.BooleanField(default = False)

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Tags"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.replace(" ","-").lower()
        super().save(*args, **kwargs)  # Call the "real" save() method.
    
    def __str__(self):
        return self.name

class Collection(models.Model):
    def __str__(self):
        return self.publication.title

   #interaction = models.PositiveIntegerField( default=0, )
  

class Setting(models.Model):

    def __str__(self):
        return self.publication.title

#    pub = models.OneToOneField(Publication, on_delete=models.CASCADE, related_name='setting' )

class Product(models.Model):
    setting = models.ForeignKey(Setting, null=True, blank= True, on_delete=models.SET_NULL, related_name='products')
    collection = models.ForeignKey(Collection, null=True, blank= True, on_delete=models.SET_NULL, related_name='products')
    price = models.PositiveIntegerField( default=0, )
    samplable = models.BooleanField ( default=True, )

    def __str__(self):
        return self.publication.title

    # wait time
    # enabled to sampler
    # min ammount

class Post(models.Model):
    pass
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

class Shipping(models.Model):
    user = models.ForeignKey(User,  verbose_name="User", null=True, on_delete=models.SET_NULL)
    STATE = (
        ('I', 'Inviato'),
        ('P', 'In Preparazione'),
        ('S', 'Spedito'),
        ('L', 'Lost'),
        ('R', 'Ricevuto'),
        ('K', 'Confermato'),
    ) 

class Sampler(models.Model):
    
    STATE = (
        ('S', 'Inviato'),
        ('P', 'In Preparazione'),
        ('S', 'Spedito'),
        ('L', 'Lost'),
        ('R', 'Ricevuto'),
        ('K', 'Confermato'),
    ) 
    pass

class Chart(models.Model):
    pass

class Order(models.Model):
    pass

class Question(models.Model):
    pass




class Publication(models.Model):
    title = models.CharField(max_length=200, unique = True)
    content = models.TextField()
    create_date = models.DateTimeField("date created", auto_now_add=True)
    publish_date = models.DateTimeField("date published", auto_now_add=False)
    tag = models.ForeignKey(Tag, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT,related_name='publication' )
    slug = models.CharField(max_length=200, unique=True)
    #author = models.ForeignKey( User,blank = True, on_delete=models.CASCADE )
    collection = models.OneToOneField(Collection,blank = True,  null = True,on_delete=models.CASCADE, related_name='publication' )
    product = models.OneToOneField(Product, blank = True, null = True,on_delete=models.CASCADE, related_name='publication' )
    setting = models.OneToOneField(Setting, blank = True, null = True,on_delete=models.CASCADE, related_name='publication' )

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

