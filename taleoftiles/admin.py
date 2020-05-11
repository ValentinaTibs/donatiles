from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django_reverse_admin import ReverseModelAdmin

from taleoftiles.models import  Product,Tag, Publication, Photo, Icon, TechnicalSpec, Catalogue

def duplicate(modeladmin, request, queryset):
    for e in queryset:
        e.pk = None
        e.slug = e.slug + "_COPY"
        e.save() 

duplicate.short_description = "Duplicate selected items"

class PhotoStackedAdmin(admin.StackedInline):
    model = Photo

    list_display = ('name', 'thumb_', )
    search_fields = ('name', )
    readonly_fields  = ( 'image_', )

class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ('name','summary','slug','in_catalogue','in_menu','in_home','public','parent','data_type')
    actions = [duplicate]

class PublicationAdminSelf(SummernoteModelAdmin):
    model = Publication
    summernote_fields = ('content',)
    fields = ('title','content','publish_date','slug')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

class PhotoAdminSelf(admin.ModelAdmin):
    model = Photo

class IconAdminSelf(admin.ModelAdmin):
    model = Icon
    list_display = ('name','image_','description')

class CatalogueAdmin(admin.ModelAdmin):
    model = Catalogue
    list_display = ('title','active')
    
class ProductAdmin(admin.ModelAdmin):
    inlines = (PhotoStackedAdmin,)
    #inlines = (PublicationAdmin,ImageStackedAdmin)
    list_display = ('name','price','color','tags', 'is_decor' )

    def name(self, obj):
        pub = obj.publication
        return pub.title

    def tags(self, obj):
        pub = obj.publication
        return "\n".join([p.name for p in pub.tag.all()])    

class TechnicalSpecAdmin(admin.ModelAdmin):
    model = TechnicalSpec
    list_display = ('slug','file','icons_',)

    def icons_(self, obj):
        return "\n".join([p.name for p in obj.icons.all()])    

admin.site.register(Tag,TagAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Publication,PublicationAdminSelf)
admin.site.register(Photo,PhotoAdminSelf)
admin.site.register(Icon,IconAdminSelf)
admin.site.register(TechnicalSpec,TechnicalSpecAdmin)
admin.site.register(Catalogue,CatalogueAdmin)


# from .models import Post, Publication, Product, Image, Tag, Setting, Collection
# from .models import Sampler, Sample, Config, Shipping, Chart, ChartItem

# from .models import Format, Color, Finish, TecnicalSpec

# class TecnicalSpecStackedAdmin(admin.StackedInline):
#     model = TecnicalSpec



# class ImageAdmin(admin.ModelAdmin):
#     model = Image

#     list_display = ('name', 'thumb_', )
#     search_fields = ('name', )
#     readonly_fields  = ( 'image_', )

# class ProductAdmin(admin.ModelAdmin):
#     model = Product

#     # list_display = ('name', )
#     # search_fields = ('slug', )

# class FormatAdmin(admin.ModelAdmin):
#     model = Format

# class ColorAdmin(admin.ModelAdmin):
#     model = Color

# class FinishAdmin(admin.ModelAdmin):
#     model = Finish

# class TecnicalSpecAdmin(SummernoteModelAdmin):
#     model = TecnicalSpec

#     summernote_fields = ('note',)




# class PublicationAdminSelf(admin.ModelAdmin):
#     inlines = (ImageStackedAdmin)
#     list_display = ('title','tags','post_id')

#     def tags(self, obj):
#         return "\n".join([p.name for p in obj.tag.all()])

# class CollectionAdmin(admin.ModelAdmin):
#     inlines = (PublicationAdmin,ImageStackedAdmin)



 
# class SettingAdmin(admin.ModelAdmin):
#     inlines = (PublicationAdmin,ImageStackedAdmin )

# class PostAdmin(admin.ModelAdmin):
#     inlines = (PublicationAdmin,ImageStackedAdmin )
#     list_display = ('name','get_tags',  )

#     def name(self, obj):
#         pub = obj.publication
#         return pub.title

#     def get_tags(self, obj):
#         pub = obj.publication
#         return "\n".join([p.name for p in pub.tag.all()])

# class SampleAdmin(admin.ModelAdmin):
#     inlines = ()

# class ShippingAdmin(admin.ModelAdmin):
#     inlines = ()

    
# admin.site.register(Shipping)
 
# admin.site.register(Post,PostAdmin)
# admin.site.register(Image,ImageAdmin)

# admin.site.register(Sampler)
# admin.site.register(Sample)
# admin.site.register(Config)

# admin.site.register(Format, FormatAdmin)
# admin.site.register(Color, ColorAdmin)
# admin.site.register(Finish, FinishAdmin)

# admin.site.register(TecnicalSpec, TecnicalSpecAdmin)


# admin.site.register(Chart)
# admin.site.register(ChartItem)

# admin.site.register(Setting,SettingAdmin)
# admin.site.register(Collection,CollectionAdmin)

