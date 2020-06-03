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
        return mark_safe('<img src="{0}">'.format(self.imagefile.url))


    def thumb_(self):
        width = 30
        ratio = 30 / self.imagefile.width
        height = self.imagefile.height * ratio
        return mark_safe('<a href="{0}"><img src="{0}" width={1} height={2}></a>'.format(self.imagefile.url,width,height))

class Config(models.Model):
	    
	int_val= models.PositiveIntegerField( default=1,  null = True, blank=True) 
	char_val= models.CharField(max_length=100, default=1,  null = True, blank=True) 
	active = models.BooleanField(default = True)
	tag = models.CharField(max_length=20, default="-")

	def __str__(self):
		return '%s' % (self.tag,)

from sendgrid.helpers.mail import *   
from sendgrid import SendGridAPIClient
import os


class MailTemplate(models.Model):
    slug            = models.CharField(max_length=50, unique=True)
    subj            = models.CharField(max_length=250, null = False, blank=False)
    sender          = models.CharField(max_length=50,  null = False, blank=False) 
    content         = models.TextField      (max_length=500, null=True, blank=True)
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
    


