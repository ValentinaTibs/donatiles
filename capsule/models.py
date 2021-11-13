from django.db import models

# Create your models here.
from taleoftiles.models import Tag, Publication
from layout.models 		import Image

class Influencer(models.Model):
	long_name		= models.CharField(max_length=200)
	palette1   		= models.CharField(max_length=6)
	palette2  		= models.CharField(max_length=6)
	palette3   		= models.CharField(max_length=6)

#	publication = models.OneToOneField(Publication, blank = True,  null = True,on_delete=models.SET_NULL, related_name='influencer' )
	name     	= models.ForeignKey(Tag, blank = True, null = True, on_delete=models.SET_NULL, related_name='influencer' )
	logo     	= models.ForeignKey(Image, blank = True, null = True, on_delete=models.SET_NULL, related_name='influencer' )
	description	= models.ForeignKey(Publication, blank = True, null = True, on_delete=models.SET_NULL, related_name='influencer' )
