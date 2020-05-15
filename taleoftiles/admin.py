from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin
from django_reverse_admin import ReverseModelAdmin

from taleoftiles.models import  Product,Tag, Publication, Photo, Icon, Price
from taleoftiles.models import TechnicalSpec, Catalogue
from taleoftiles.forms import CustomProductModelForm

def duplicate(modeladmin, request, queryset):
    for e in queryset:
        e.pk = None
        e.slug = e.slug + "_COPY"
        e.save()

def duplicate_product(modeladmin, request, queryset):
    for e in queryset:
        cc = e.tags.all()
        e.pk = None
        e.code = e.code + "_COPY"
        e.save()
        for tag in cc:
            e.tags.add(tag)
            
duplicate.short_description = "Duplicate selected items"
duplicate_product.short_description = "Duplicate selected items"

def make_for_product(modeladmin, request, queryset):
    for e in queryset:
        e.in_product_edit = not(e.in_product_edit)
        e.save() 

make_for_product.short_description = "Toggle availability for product edit"

class PhotoStackedAdmin(admin.StackedInline):
    model = Photo

    list_display = ('name',  )
    search_fields = ('name', )

class PriceStackedAdmin(admin.StackedInline):
    model = Price

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "size":
            kwargs["queryset"] = Tag.objects.filter(parent__parent__slug='format')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class PriceAdmin(admin.ModelAdmin):

    model = Price

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "size":
            kwargs["queryset"] = Tag.objects.filter(parent__parent__slug='format')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    list_display = ("product","size","euros")

class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ('name','summary','slug','in_catalogue','in_menu','in_home','in_product_edit','public','order','parent','data_type')
    actions = [duplicate,make_for_product]

    search_fields = ('name','parent__slug','parent__parent__slug' )


class SerieAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ('name','summary','slug','in_catalogue','in_menu','in_home','in_product_edit','public','parent','data_type')
    actions = [duplicate,make_for_product]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Tag.objects.filter(parent__slug='serie')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
    form = CustomProductModelForm
    actions = [duplicate_product]
    inlines = (PriceStackedAdmin,PhotoStackedAdmin)
    list_display = ('name',
                    'wait_time',
                    'min_ammount',
                    'code',
                    'is_decor',
                    'is_samplable',
                    'available',
                    'is_active',
                    'tags_',
                    'publication',
                    'support_to',
                    'techspec'
                    )

    def name(self, obj):
        pub = obj.publication
        return pub.title

    def tags_(self, obj):
        return "\n".join([p.name + ' * ' for p in obj.tags.all()])    

class TechnicalSpecAdmin(admin.ModelAdmin):
    model = TechnicalSpec
    list_display = ('slug','file','icons_',)

    def icons_(self, obj):
        return "\n".join([p.name for p in obj.icons.all()])    

admin.site.register(Tag,TagAdmin)
# admin.site.register(Tag,SerieAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Price,PriceAdmin)
admin.site.register(Publication,PublicationAdminSelf)
admin.site.register(Photo,PhotoAdminSelf)
admin.site.register(Icon,IconAdminSelf)
admin.site.register(TechnicalSpec,TechnicalSpecAdmin)
admin.site.register(Catalogue,CatalogueAdmin)

