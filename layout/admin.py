from django.contrib import admin
from layout.models import  Element, ElementTag, MailTemplate, Image,TranslationFile
from modeltranslation.admin import TranslationAdmin
from django.conf import settings

# Register your models here.

def duplicate(modeladmin, request, queryset):
    for e in queryset:
        e.pk = None
        e.slug = e.slug + "_COPY"
        e.save()

duplicate.short_description = "Duplicate selected items"

class ElementImageStackedAdmin(admin.StackedInline):
    model = Image

    list_display = ('name',  )
    search_fields = ('name', )
    exclude = ('product','icon','is_cover','order','post' )

class ElementLayoutAdmin(TranslationAdmin):
    model = Element
    list_display = ('name', 'tags',  'data_type','public' )
    inlines = (ElementImageStackedAdmin,)
    readonly_fields  = ( 'image_', )
    
    def tags(self, obj):
        return "\n".join([p.name for p in obj.tag.all()])  

    def image_(self,obj):
        if obj and obj.is_img():
            return obj.image.image_()
        else:
            return "NO IMAGE"

class ElementTagAdmin(admin.ModelAdmin):
    model = ElementTag
    list_display = ('name', 'summary','slug','public','parent_' )
    actions = [duplicate,]

    def parent_(self, obj):
        if obj.parent:
            return obj.parent
        else:
            return "-"
from django.utils.html import format_html
from django.urls import re_path, reverse,path
from django.http import HttpResponse
from django.core.management import call_command


def compile_messages_(modeladmin, request, queryset):
    call_command('compilemessages', )
compile_messages_.short_description = "Publish messages"    

class TranslationFileAdmin(admin.ModelAdmin):
    model = TranslationFile 
    readonly_fields = ('download_link','version')
    actions = [compile_messages_,]
    
    # add custom view to urls
    def get_urls(self):
        urls = super(TranslationFileAdmin, self).get_urls()
        urls += [
            path("download-file/<str:lan>",  self.download_file, name="download_translations"),

        ]
        return urls

    # custom "field" that returns a link to the custom function
    def download_link(self, obj):
        fin_string = ""
        for lan in settings.LANGUAGES:
            address = reverse('admin:download_translations', args=[lan[0]])
            ext_string =  "<a href="+address+">Download "+ str(lan[1]) +"   </a>"
            fin_string = fin_string +ext_string
        
        return format_html(fin_string)

    # def compile_messages(self,obj):
    #     call_command('compilemessages', )


    # add custom view function that downloads the file
    def download_file(self, request, lan):
        response = HttpResponse(content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="translate_'+lan+'.po"'
        # generate dynamic file content using object pk
        with open(settings.LOCALE_PATHS[0]+'/'+lan+'/LC_MESSAGES/django.po', 'r') as file1:
            response.write(file1.read())
        return response


        
class MailTemplateAdmin(admin.ModelAdmin):
    model = MailTemplate
    list_display = ("slug","subj","sender","content","template_id","template_vs","no_reply",)

class ImageAdminSelf(admin.ModelAdmin):
    model = Image
    readonly_fields  = ( 'image_',)

admin.site.register(Element,ElementLayoutAdmin)
admin.site.register(ElementTag,ElementTagAdmin)
admin.site.register(MailTemplate,MailTemplateAdmin)
admin.site.register(TranslationFile,TranslationFileAdmin)

admin.site.register(Image,ImageAdminSelf)
