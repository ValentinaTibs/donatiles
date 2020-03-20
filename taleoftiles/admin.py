from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django_reverse_admin import ReverseModelAdmin

from .models import Post, Publication, Product, Image, Tag, Setting, Collection
from .models import Sampler, Sample, Config, Shipping, Chart, ChartItem

from .models import Format, Color, Finish, TecnicalSpec

class TecnicalSpecStackedAdmin(admin.StackedInline):
    model = TecnicalSpec

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

class FormatAdmin(admin.ModelAdmin):
    model = Format

class ColorAdmin(admin.ModelAdmin):
    model = Color

class FinishAdmin(admin.ModelAdmin):
    model = Finish

class TecnicalSpecAdmin(SummernoteModelAdmin):
    model = TecnicalSpec

    summernote_fields = ('note',)

class TagAdmin(admin.ModelAdmin):
    model = Tag
    exclude = ('slug',)
    list_display = ('name','summary','slug')

class PublicationAdmin(admin.StackedInline):
    model = Publication

class PublicationAdminSelf(admin.ModelAdmin):
    list_display = ('title','tags','post_id')

    def tags(self, obj):
        return "\n".join([p.name for p in obj.tag.all()])


class CollectionAdmin(admin.ModelAdmin):
    inlines = (PublicationAdmin,ImageStackedAdmin)

class ProductAdmin(admin.ModelAdmin):
    inlines = (PublicationAdmin,ImageStackedAdmin)
    list_display = ('name','price','color','tags', 'is_decor' )

    def name(self, obj):
        pub = obj.publication
        return pub.title

    def tags(self, obj):
        pub = obj.publication
        return "\n".join([p.name for p in pub.tag.all()])

 
class SettingAdmin(admin.ModelAdmin):
    inlines = (PublicationAdmin,ImageStackedAdmin )

class PostAdmin(admin.ModelAdmin):
    inlines = (PublicationAdmin,ImageStackedAdmin )
    list_display = ('name','get_tags',  )

    def name(self, obj):
        pub = obj.publication
        return pub.title

    def get_tags(self, obj):
        pub = obj.publication
        return "\n".join([p.name for p in pub.tag.all()])

class SampleAdmin(admin.ModelAdmin):
    inlines = ()

class ShippingAdmin(admin.ModelAdmin):
    inlines = ()

    
admin.site.register(Shipping)
 
admin.site.register(Post,PostAdmin)
admin.site.register(Image,ImageAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Sampler)
admin.site.register(Sample)
admin.site.register(Config)

admin.site.register(Format, FormatAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Finish, FinishAdmin)

admin.site.register(TecnicalSpec, TecnicalSpecAdmin)


admin.site.register(Chart)
admin.site.register(ChartItem)

admin.site.register(Setting,SettingAdmin)
admin.site.register(Collection,CollectionAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Publication,PublicationAdminSelf)

