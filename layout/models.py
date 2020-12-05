from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from taleoftiles.models import Product, Tag, TechnicalSpec
from blog.models import Post
from PIL import Image 
from django.conf import settings

import sys
import os

from django.core.management import call_command

DATA_TYPE = (
    ('t', 'Text'),
    ('i', 'Image')
) 

class TranslationFile(models.Model):

    content     = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.

        with open(settings.LOCALE_PATHS[0]+'/filename.po', 'w') as f:
            print("opened")
            f.write(self.content)
        call_command('compilemessages', )


class ElementTag(models.Model):
    name    = models.CharField  (max_length=200)
    slug    = models.CharField  (max_length=200, unique=True)
    public  = models.BooleanField(default = True)
    summary = models.CharField  (max_length=200, null=True, blank=True,)
    parent  = models.ForeignKey ("self",         null=True, blank=True, on_delete=models.SET_NULL, related_name='childs' )    
    
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

    def is_img(self):
        if self.data_type == 'i':
            return True
        return False    
    
    def data(self):
        if self.data_type == 'i' and  self.image and self.is_img() :
            return self.image.imagefile.url
        return self.content    

    def image_(self):
        return self.image.image_()


    def thumb_(self):
        return  self.image.thumb_()

class Config(models.Model):
	    
	int_val    = models.PositiveIntegerField( default=1,  null = True, blank=True) 
	char_val   = models.CharField(max_length=100, default=1,  null = True, blank=True) 
	active     = models.BooleanField(default = True)
	tag        = models.CharField(max_length=20, default="-")

	def __str__(self):
		return '%s' % (self.tag,)

import os
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, To, Subject, PlainTextContent, HtmlContent, SendGridException

from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.utils import translation
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from python_http_client import exceptions

import logging



class MailTemplate(models.Model):
    slug            = models.CharField(max_length=50, unique=True)
    subj            = models.CharField(max_length=250, null = False, blank=False)
    sender          = models.CharField(max_length=50,  null = False, blank=False) 
    content         = models.TextField(max_length=500, null=True, blank=True)
    template_id     = models.CharField(max_length=50, null = False, blank=False) 
    template_vs     = models.CharField(max_length=50, null = False, blank=False) 
    no_reply        = models.BooleanField(default = False)

    def send_password_reset(self,user):
        cLng = translation.get_language()
        email_template_name = "email/"+cLng+"/password_reset_email.txt"
        c = {
                "email":user.email,
                'domain':'www.taleoftiles.com',
                'site_name': 'TaleOfTiles',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                }
        email = render_to_string(email_template_name, c)

        message = Mail(from_email=From('info@taleoftiles.com', 'TaleOfTiles'),
                to_emails=To(user.email, user.email),
                subject=Subject("Password Reset"),
                html_content=HtmlContent(email))

        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        try:
            response = sg.send(message)
        except exceptions.BadRequestsError as e:
            logger = logging.getLogger('email')
            logger.error(e.body)

    def send_order(self,request,user,order):
        cLng = translation.get_language()
        email_template_name = "email/"+cLng+"/order_email.txt"
        c = {
                "order_id":order.internal_tracking_id,
                'domain':'www.taleoftiles.com',
                'site_name': 'TaleOfTiles',
                "user": user,
                }
        
        email = render_to_string(email_template_name, c)
        message = Mail(from_email=From('info@taleoftiles.com', 'TaleOfTiles'),
                to_emails=To(user.email, user.email),
                subject=Subject("Order num."+ order.internal_tracking_id+" Received "),
                html_content=HtmlContent(email))

        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        try:
            response = sg.send(message)

        except exceptions.BadRequestsError as e:
            logger = logging.getLogger('email')
            logger.error(e.body)

    def send_register(self,user,one_time_pwd):
        cLng = translation.get_language()
        email_template_name = "email/"+cLng+"/register_email.txt"
        c = {
                'domain':'www.taleoftiles.com',
                'site_name': 'TaleOfTiles',
                'pwd':one_time_pwd,
                "user": user,
                }
        email = render_to_string(email_template_name, c)

        message = Mail(from_email=From('info@taleoftiles.com', 'TaleOfTiles'),
                to_emails=To(user.email, user.email),
                subject=Subject("Welcome in TaleOfTiles"),
                html_content=HtmlContent(email))

        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        
        try:
            response = sg.send(message)
        except exceptions.BadRequestsError as e:
            logger = logging.getLogger('email')
            logger.error(e.body)


    def send_welcome(self,user):
        cLng = translation.get_language()
        email_template_name = "email/"+cLng+"/welcome_email.txt"
        c = {
                'domain':'www.taleoftiles.com',
                'site_name': 'TaleOfTiles',
                "user": user,
                }
        email = render_to_string(email_template_name, c)

        message = Mail(from_email=From('info@taleoftiles.com', 'TaleOfTiles'),
                to_emails=To(user.email, user.email),
                subject=Subject("Welcome in TaleOfTiles"),
                html_content=HtmlContent(email))

        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        try:
            response = sg.send(message)
        except exceptions.BadRequestsError as e:
            logger = logging.getLogger('email')
            logger.error(e.body)



 
class Icon(models.Model):  
    name        = models.CharField (max_length = 100 , null = False, blank=False, unique=True)
    description = models.TextField()
    tag         = models.OneToOneField  (Tag,  blank = True, null = True, on_delete=models.SET_NULL, related_name='icons' )
    techspecs   = models.ManyToManyField(TechnicalSpec,  blank= True, related_name='icons')
    
    def image_(self):
        return self.image.image_()

    def __str__(self):
        return '%s' % (self.name, )


# class CoverManager(models.Manager):
#     def get_queryset(self):
#         qs = super().get_queryset().filter(is_cover = True)
#         return qs

class Image(models.Model):  

    name        = models.CharField (max_length = 100 , null = True, blank=True)
    imagefile   = models.ImageField( upload_to='photos', null=True, blank=True, help_text="Load an image.")
    thumbnail   = models.ImageField( upload_to='thumbs', null=True, editable=False)
    product     = models.ForeignKey     (Product,   blank = True, null = True,on_delete=models.SET_NULL, related_name='images' )
    element     = models.OneToOneField  (Element,   blank = True, null = True,on_delete=models.SET_NULL, related_name='image' )
    icon        = models.OneToOneField  (Icon,      blank = True, null = True,on_delete=models.SET_NULL, related_name='image' )
    post        = models.OneToOneField  (Post,      blank = True, null = True,on_delete=models.SET_NULL, related_name='cover' )
    
    order       = models.PositiveIntegerField( default=0, )   
    is_cover    = models.BooleanField(default = False)

    format_tag  = models.ForeignKey  (Tag,  blank = True, null = True, on_delete=models.SET_NULL, related_name='format_images' )
    finish_tag  = models.ForeignKey  (Tag,  blank = True, null = True, on_delete=models.SET_NULL, related_name='finish_images' )


    class Meta:
        ordering = ["order"]    

    def image_(self):
        if self.imagefile:
            return mark_safe('<img src="{0}" style="width : 100%;">'.format(self.imagefile.url))
        else :
            return mark_safe('<p>No image available</p>')

    def thumb_(self):
        if not self.imagefile:
            return 'images/products/productthumb.png'
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
        
        # if not self.make_thumbnail():
        #     return
        #     #raise Exception('Could not create thumbnail - is the file type valid?')

    # def make_thumbnail(self):

    #     image = Image.open(self.imagefile)
    #     image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

    #     thumb_name, thumb_extension = os.path.splitext(self.photo.name)
    #     thumb_extension = thumb_extension.lower()

    #     thumb_filename = thumb_name + '_thumb' + thumb_extension

    #     if thumb_extension in ['.jpg', '.jpeg']:
    #         FTYPE = 'JPEG'
    #     elif thumb_extension == '.gif':
    #         FTYPE = 'GIF'
    #     elif thumb_extension == '.png':
    #         FTYPE = 'PNG'
    #     else:
    #         return False    # Unrecognized file type

    #     # Save thumbnail to in-memory file as StringIO
    #     temp_thumb = BytesIO()
    #     image.save(temp_thumb, FTYPE)
    #     temp_thumb.seek(0)

    #     # set save=False, otherwise it will run in an infinite loop
    #     self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
    #     temp_thumb.close()

    #     return True


