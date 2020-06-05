from django.db import models
from taleoftiles.models import Tag, Publication, Product

import datetime as dt

class ActivePostManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().filter(publication__publish_date__lte= dt.datetime.now(), deleted = False)
        return qs

class Post(models.Model):
    tags        = models.ManyToManyField(Tag, blank= True, related_name='posts')
    publication = models.OneToOneField(Publication, blank = True,  null = True,on_delete=models.CASCADE, related_name='post' )
    related_products = models.ManyToManyField(Product, blank= True, related_name='posts')

    deleted = models.BooleanField(default = False)
    order  = models.PositiveIntegerField( default=0, )   
    in_home = models.BooleanField(default = False)

    objects = models.Manager() # The default manager.
    active  = ActivePostManager() # The Active Charts

    def in_home(self):
    	return self.tags.filter(slug='in-home').count()>0

    def __str__(self):
        return self.publication.title


