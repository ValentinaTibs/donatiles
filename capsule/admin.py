from django.contrib import admin
from capsule.models import Influencer

# Register your models here.
class InfluencerAdmin(admin.ModelAdmin):
    model = Influencer
    list_display = ("long_name","name","palette1","palette2","palette3","logo","description",)
admin.site.register(Influencer,InfluencerAdmin)
