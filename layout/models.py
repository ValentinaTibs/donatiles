from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from taleoftiles.models import Product, Tag, TechnicalSpec

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
    tag         = models.ManyToManyField(ElementTag, related_name='element')

    def __str__(self):
        return self.name    
    
    def data(self):
        if self.data_type == 'i':
            return self.image.image_()
            return self.image.imagefile.url
        return self.content
        # if self.data_type == 't':
        #     return '%s' % (self.content,)   
        # if self.data_type == 'i':
        #     return self.image.imagefile.url
    

    def image_(self):
        return self.image.image_()


    def thumb_(self):
        return " "
        return  self.image.thumb_()

class Config(models.Model):
	    
	int_val    = models.PositiveIntegerField( default=1,  null = True, blank=True) 
	char_val   = models.CharField(max_length=100, default=1,  null = True, blank=True) 
	active     = models.BooleanField(default = True)
	tag        = models.CharField(max_length=20, default="-")

	def __str__(self):
		return '%s' % (self.tag,)

from sendgrid.helpers.mail import *   
from sendgrid import SendGridAPIClient
import os


class MailTemplate(models.Model):
    slug            = models.CharField(max_length=50, unique=True)
    subj            = models.CharField(max_length=250, null = False, blank=False)
    sender          = models.CharField(max_length=50,  null = False, blank=False) 
    content         = models.TextField(max_length=500, null=True, blank=True)
    template_id     = models.CharField(max_length=50, null = False, blank=False) 
    template_vs     = models.CharField(max_length=50, null = False, blank=False) 
    no_reply        = models.BooleanField(default = False)


    def send(self,email_rec,pwd):
        pass

        message = Mail()
        message.to_emails = To("tibaldo.valentina@gmail.com")
        message.subject = Subject(self.subj, p=0)
        message.from_email = Email(self.sender)
        message.html_content = HtmlContent(self.content)

        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)

        except Exception as e:
            print(str(e))
            print(str(e.body))

        # mail_settings               = MailSettings()
        # mail_settings.sandbox_mode  = SandBoxMode(True)
        # message.mail_settings       = mail_settings
        # message.template_id         = TemplateId(self.template_id)

        # message.substitution = Substitution('content', self.content, p=0)
        # message.substitution = Substitution('password', pwd, p=0)


    def send_first_password(self,email_rec,pwd):
        da_mail = MailTemplate.objects.filter(slug='first-password').first()
        da_mail.send(email_rec, pwd)
    
    def send_password_reset(self,email_rec):
        da_mail = MailTemplate.objects.filter(slug='password-reset').first()
        da_mail.send(email_rec)
    

class Icon(models.Model):  
    name        = models.CharField (max_length = 100 , null = False, blank=False, unique=True)
    description = models.TextField()
    tag         = models.OneToOneField  (Tag,  blank = True, null = True, on_delete=models.SET_NULL, related_name='icons' )
    techspecs   = models.ManyToManyField(TechnicalSpec,  blank= True, related_name='icons')
    
    def image_(self):
        return self.image.image_()

    def __str__(self):
        return '%s' % (self.name, )

class Image(models.Model):  

    name        = models.CharField (max_length = 100 , null = True, blank=True)
    imagefile   = models.ImageField( upload_to='photos', null=True, blank=True, help_text="Load an image.")
    product     = models.ForeignKey     (Product,   blank = True, null = True,on_delete=models.SET_NULL, related_name='images' )
    element     = models.OneToOneField  (Element,   blank = True, null = True,on_delete=models.SET_NULL, related_name='image' )
    icon        = models.OneToOneField  (Icon,      blank = True, null = True,on_delete=models.SET_NULL, related_name='image' )
    order       = models.PositiveIntegerField( default=0, )   
    is_cover    = models.BooleanField(default = False)

    class Meta:
        ordering = ["order"]    

    def image_(self):
        if self.imagefile:
            return mark_safe('<img src="{0}" style="width : 100%;">'.format(self.imagefile.url))
        else :
            return mark_safe('<p>No image available</p>')

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

