from django.contrib import admin
from layout.models import  Element, ElementTag
from modeltranslation.admin import TranslationAdmin

# Register your models here.
class ElementLayoutAdmin(TranslationAdmin):
    model = Element
    list_display = ('name', 'tag', 'tag__parent', 'data_type','public' )
    readonly_fields  = ( 'image_', )

    def tag__parent(self, obj):

        if obj.tag:
            return obj.tag.parent
        else:
            return "-"
    
class ElementTagAdmin(admin.ModelAdmin):
    model = ElementTag
    list_display = ('name', 'summary','slug','public','parent_' )

    def parent_(self, obj):
        if obj.parent:
            return obj.parent
        else:
            return "-"
    

admin.site.register(Element,ElementLayoutAdmin)
admin.site.register(ElementTag,ElementTagAdmin)
