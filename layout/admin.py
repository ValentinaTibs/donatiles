from django.contrib import admin
from layout.models import  Element, ElementTag
from modeltranslation.admin import TranslationAdmin

# Register your models here.
class ElementLayoutAdmin(TranslationAdmin):
    model = Element
    list_display = ('name', 'tag', )
    
class ElementTagAdmin(admin.ModelAdmin):
    model = ElementTag

admin.site.register(Element,ElementLayoutAdmin)
admin.site.register(ElementTag,ElementTagAdmin)
