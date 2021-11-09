from django.contrib import admin
from capsule.models import Influencer

# Register your models here.
class InfluencerAdmin(admin.ModelAdmin):
    model = Influencer

admin.site.register(Influencer,InfluencerAdmin)
