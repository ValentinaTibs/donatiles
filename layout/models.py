from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

DATA_TYPE = (
    ('t', 'Text'),
    ('i', 'Image')
) 

class ElementTag(models.Model):
    name    = models.CharField  (max_length=200)
    slug    = models.CharField  (max_length=200, unique=True)
    public  = models.BooleanField(default = True)
    summary = models.CharField  (max_length=200, null=True, blank=True,)
    parent  = models.ForeignKey ("self",        null=True, blank=True, on_delete=models.SET_NULL, related_name='childs' )    
    
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
    name        = models.CharField      (max_length=200)
    content     = models.TextField      (max_length=200, null=True, blank=True)
    public      = models.BooleanField   (default = True)
    data_type   = models.CharField      (choices=DATA_TYPE, max_length=2,  default=DATA_TYPE[0])
    imagefile   = models.ImageField     (upload_to='img',null=True, blank=True, help_text="Load an image.")
    tag         = models.ManyToManyField(ElementTag, related_name='element')

    def __str__(self):
        if self.data_type == 't':
        	return '%s' % (self.content,)   
        if self.data_type == 'i':
            return self.imagefile.url
    
    def data(self):
        if self.data_type == 'i':
            return self.imagefile
        return self.content

    def image_(self):
        return mark_safe('<img src="/media/{0}">'.format(self.imagefile))

    def thumb_(self):
        width = 30
        ratio = 30 / self.imagefile.width
        height = self.imagefile.height * ratio
        return mark_safe('<a href="/media/{0}"><img src="/media/{0}" width={1} height={2}></a>'.format(self.imagefile,width,height))

class Config(models.Model):
	    
	int_val= models.PositiveIntegerField( default=1,  null = True, blank=True) 
	char_val= models.CharField(max_length=100, default=1,  null = True, blank=True) 
	active = models.BooleanField(default = True)
	tag = models.CharField(max_length=20, default="-")

	def __str__(self):
		return '%s' % (self.tag,)
