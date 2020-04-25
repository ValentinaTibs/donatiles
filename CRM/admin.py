from django.contrib import admin
from CRM.models import Profile

class ClientAdmin(admin.ModelAdmin):
    model = Profile

admin.site.register(Profile,ClientAdmin)