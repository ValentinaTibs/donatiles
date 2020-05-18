from django.contrib import admin
from layout.models import  Element, ElementTag
from modeltranslation.admin import TranslationAdmin

# Register your models here.

def duplicate(modeladmin, request, queryset):
    for e in queryset:
        e.pk = None
        e.slug = e.slug + "_COPY"
        e.save()

duplicate.short_description = "Duplicate selected items"

class ElementLayoutAdmin(TranslationAdmin):
    model = Element
    list_display = ('name', 'tags',  'data_type','public' )
    readonly_fields  = ( 'image_', )
    
    def tags(self, obj):
        return "\n".join([p.name for p in obj.tag.all()])  

class ElementTagAdmin(admin.ModelAdmin):
    model = ElementTag
    list_display = ('name', 'summary','slug','public','parent_' )
    actions = [duplicate,]

    def parent_(self, obj):
        if obj.parent:
            return obj.parent
        else:
            return "-"
    

admin.site.register(Element,ElementLayoutAdmin)
admin.site.register(ElementTag,ElementTagAdmin)
