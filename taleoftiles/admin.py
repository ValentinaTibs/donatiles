from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django_reverse_admin import ReverseModelAdmin

from .models import Post, Publication, Product, Image, Tag, Setting, Collection
from .models import Sampler, Sample, Config, Shipping, Chart, ChartItem

from .models import Format, Color, Finish

class ImageStackedAdmin(admin.StackedInline):
    model = Image

    list_display = ('name', 'thumb_', )
    search_fields = ('name', )
    readonly_fields  = ( 'image_', )

class ImageAdmin(admin.ModelAdmin):
    model = Image

    list_display = ('name', 'thumb_', )
    search_fields = ('name', )
    readonly_fields  = ( 'image_', )

class ProductAdmin(admin.ModelAdmin):
    model = Product

    list_display = ('name', )
    search_fields = ('slug', )


class TagAdmin(admin.ModelAdmin):
    model = Tag
    exclude = ('slug',)

class PublicationAdmin(admin.StackedInline):
    model = Publication
    exclude = ('slug',)

class CollectionAdmin(admin.ModelAdmin):
    inlines = (PublicationAdmin,ImageStackedAdmin)

class ProductAdmin(admin.ModelAdmin):
    inlines = (PublicationAdmin,ImageStackedAdmin)
 
class SettingAdmin(admin.ModelAdmin):
    inlines = (PublicationAdmin,ImageStackedAdmin )

class SampleAdmin(admin.ModelAdmin):
    inlines = ()

class ShippingAdmin(admin.ModelAdmin):
    inlines = ()

    
admin.site.register(Shipping)
 
admin.site.register(Post)
admin.site.register(Image,ImageAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Sampler)
admin.site.register(Sample)
admin.site.register(Config)

admin.site.register(Format)
admin.site.register(Color)
admin.site.register(Finish)

admin.site.register(Chart)
admin.site.register(ChartItem)

admin.site.register(Setting,SettingAdmin)
admin.site.register(Collection,CollectionAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Publication)

