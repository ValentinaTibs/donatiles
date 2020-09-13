from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin
from django_reverse_admin import ReverseModelAdmin

from taleoftiles.models import  Product, Tag, Publication, Price
from taleoftiles.models import TechnicalSpec, Catalogue
from layout.models      import Image, Icon

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

def duplicate_plain(modeladmin, request, queryset):
    for e in queryset:
        e.pk = None
        e.save()
            
duplicate.short_description = "Duplicate selected items"
duplicate_product.short_description = "Duplicate selected items"
duplicate_plain.short_description = "Duplicate selected items"

def make_for_product(modeladmin, request, queryset):
    for e in queryset:
        e.in_product_edit = not(e.in_product_edit)
        e.save() 

make_for_product.short_description = "Toggle availability for product edit"

class PhotoStackedAdmin(admin.StackedInline):
    model = Image

    list_display = ('name',  )
    search_fields = ('name', )
    exclude = ('name','element','icon','post' )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "format_tag":
            kwargs["queryset"] = Tag.objects.filter(parent__parent__slug='format').order_by('-slug')
        if db_field.name == "finish_tag":
            kwargs["queryset"] = Tag.objects.filter(parent__parent__slug='finish').order_by('-slug')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class IconImageStackedAdmin(admin.StackedInline):
    model = Image

    list_display = ('name',  )
    search_fields = ('name', )
    exclude = ('name','product','is_cover','order','element' )


class PriceStackedAdmin(admin.StackedInline):
    model = Price

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "size":
            kwargs["queryset"] = Tag.objects.filter(parent__parent__slug='format')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class PriceAdmin(admin.ModelAdmin):

    model = Price
    actions = [duplicate_plain,]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "size":
            kwargs["queryset"] = Tag.objects.filter(parent__parent__slug='format')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    list_display = ("product","size","euros","m2_box","weight_box")

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
    summernote_fields = ('content_it','content_de','content_en','content_sv',)
    fields = ('title_it','title_de','title_en','title_sv','content_it','content_de','content_en','content_sv',
        'publish_date','slug')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

    list_display = ('title_', 'slug')

    def title_(self, obj):
        if obj.title == '':
            return '-'
        return obj.title

class IconAdminSelf(admin.ModelAdmin):
    model = Icon
    inlines = (IconImageStackedAdmin,)
    list_display = ('name','image_','description')

class CatalogueAdmin(admin.ModelAdmin):
    model = Catalogue
    list_display = ('title','active')
    

class ProductAdmin(admin.ModelAdmin):
    form = CustomProductModelForm
    actions = [duplicate_product]
    inlines = (PriceStackedAdmin,PhotoStackedAdmin)

    search_fields = ('name', 'code','publication')
    
    list_display = ('name_',
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
    def name_(self, obj):
        if obj.name == " ":
            return obj.code
        return obj.name

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

admin.site.register(Icon,IconAdminSelf)
admin.site.register(TechnicalSpec,TechnicalSpecAdmin)
admin.site.register(Catalogue,CatalogueAdmin)

