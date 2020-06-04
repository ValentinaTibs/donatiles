from django.contrib import admin
from layout.models import  Element, ElementTag, MailTemplate, Image
from modeltranslation.admin import TranslationAdmin

# Register your models here.

def duplicate(modeladmin, request, queryset):
    for e in queryset:
        e.pk = None
        e.slug = e.slug + "_COPY"
        e.save()

duplicate.short_description = "Duplicate selected items"

class ImageStackedAdmin(admin.StackedInline):
    model = Image

    list_display = ('name',  )
    search_fields = ('name', )
    exclude = ('product','icon','is_cover' )


class ElementLayoutAdmin(TranslationAdmin):
    model = Element
    list_display = ('name', 'tags',  'data_type','public' )
    inlines = (ImageStackedAdmin,)
    readonly_fields  = ( 'image__image_', )
    
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
    
class MailTemplateAdmin(admin.ModelAdmin):
    model = MailTemplate
    list_display = ("slug","subj","sender","content","template_id","template_vs","no_reply",)

class ImageAdminSelf(admin.ModelAdmin):
    model = Image
    readonly_fields  = ( 'image_',)

admin.site.register(Element,ElementLayoutAdmin)
admin.site.register(ElementTag,ElementTagAdmin)
admin.site.register(MailTemplate,MailTemplateAdmin)
admin.site.register(Image,ImageAdminSelf)
