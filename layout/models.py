from django.db import models
from django.utils.translation import ugettext_lazy as _

DATA_TYPE = (
    ('t', 'Text'),
    ('i', 'Image')
) 

class ElementTag(models.Model):
    name = models.CharField(max_length=200)
    summary = models.CharField(max_length=200, null = True, blank=True,)
    slug = models.CharField(max_length=200,  unique=True)
    public = models.BooleanField(default = True)
    parent = models.ForeignKey("self", blank = True, null = True,on_delete=models.SET_NULL, related_name='childs' )    
    
    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Tags"
        #ordering = ["order"] 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.replace(" ","-").lower()
        super().save(*args, **kwargs)  # Call the "real" save() method.
    
    def __str__(self):
        return self.name

class Element(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField(max_length=200)
    imagefile = models.ImageField( upload_to='img', null=True, blank=True, help_text="Load an image.")
    public = models.BooleanField(default = True)
    data_type   = models.CharField(max_length=2, choices=DATA_TYPE, default='t')
    
    tag = models.ForeignKey(ElementTag, blank = True, null = True,on_delete=models.SET_NULL, related_name='element' )

    def __str__(self):
        if data_type == 't'
        	return '%s' % (self.name,)   
        if data_type == 'i'
            return mark_safe('<img src="/img/{0}">'.format(self.imagefile))

    def image_(self):
        return mark_safe('<img src="/img/{0}">'.format(self.imagefile))

class Config(models.Model):
	    
	int_val= models.PositiveIntegerField( default=1,  null = True, blank=True) 
	char_val= models.CharField(max_length=100, default=1,  null = True, blank=True) 
	active = models.BooleanField(default = True)
	tag = models.CharField(max_length=20, default="-")

	def __str__(self):
		return '%s' % (self.tag,)

   


# class Image(models.Model):  
#     name =  models.CharField (max_length = 100 , null = True, blank=True)
#     imagefile = models.ImageField( upload_to='img', null=True, blank=True, help_text="Load an image.")
#     elm = models.ForeignKey(Element, blank = True, null = False, on_delete=models.SET_NULL, related_name='image' )

#     def image_(self):
#         return mark_safe('<img class="'+self.elm.name+'" src="/media/{0}">'.format(self.imagefile))

#     def __str__(self):
#         return '%s' % (self.name,)

#     def save(self, *args, **kwargs):
#         if(self.name == None):
#             self.name = self.imagefile.name
#         super().save(*args, **kwargs)  # Call the "real" save() method.