from django.db import models

# Create your models here.
from taleoftiles.models import Publication, Product

class Influencer(models.Model):
	name   		= models.CharField(max_length=200)
	slug		= models.CharField(max_length=200, unique=True, blank=True,null=False)
	publication = models.OneToOneField(Publication, blank = True,  null = True,on_delete=models.SET_NULL, related_name='influencer' )
	product     = models.ForeignKey(Product, blank = True, null = True, on_delete=models.SET_NULL, related_name='influencer' )

	def in_home(self):
		return self.tags.filter(slug='in-home').count()>0

	def __str__(self):
		return self.publication.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self.name.replace(" ","-").lower()
		return super().save(*args, **kwargs)  # Call the "real" save() method.
