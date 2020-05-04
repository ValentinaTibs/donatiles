from django.db import models
from taleoftiles.models import Tag, Publication

# Create your models here.
class Post(models.Model):
    tags = models.ManyToManyField(Tag, blank= True, related_name='posts')
    publication = models.OneToOneField(Publication, blank = True,  null = True,on_delete=models.CASCADE, related_name='post' )
    deleted = models.BooleanField(default = False)

    def __str__(self):
        return self.publication.title