from django.contrib import admin
from layout.models import  Element, ElementTag
from modeltranslation.admin import TranslationAdmin

# Register your models here.
class ElementLayoutAdmin(admin.ModelAdmin):
    model = Element
    list_display = ('name', 'tag', )
    
class ElementTagAdmin(TranslationAdmin):
    model = ElementTag


admin.site.register(Element,ElementLayoutAdmin)
admin.site.register(ElementTag,ElementTagAdmin)
