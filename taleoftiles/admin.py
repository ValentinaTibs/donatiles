from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin
from django_reverse_admin import ReverseModelAdmin

from taleoftiles.models import  Product, Tag, Publication, Price, EasyProductProxy
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

from django.core.exceptions import ObjectDoesNotExist
def toggle_handmade(modeladmin, request, queryset):
    hm = Tag.objects.get(slug='handmade')
    for product in queryset:
        try: 
            handmades_tag = product.tags.get(slug='handmade_button') 
        except ObjectDoesNotExist:
            continue
        product.tags.add(hm.pk)
        product.tags.remove(handmades_tag.pk)
        product.save()

def tagga_terracotta(modeladmin, request, queryset):
    hm = Tag.objects.get(slug='cotto')
    for product in queryset:
        product.tags.add(hm.pk)
        product.save()

def toggle_samplable(modeladmin, request, queryset):
    hm = Tag.objects.get(slug='samplable')
    for product in queryset:
        if product.is_samplable:
            product.tags.add(hm.pk)
            product.save()

def assign_catalogue(modeladmin, request, queryset):
    cat = Catalogue.objects.get(title='2020')
    for product in queryset:
        if product.is_active:
            cat.products.add(product)
            cat.save()
            
# - not safe -  you should remove it all first and than add it back
def toggle_parent_format(modeladmin, request, queryset):
    #format = Tag.objects.get(slug='format')
    for product in queryset:
        for format_ in product.formats():
            product.tags.add(format_.parent)             
            product.save()

duplicate.short_description = "Duplicate selected items"
duplicate_product.short_description = "Duplicate selected items"
duplicate_plain.short_description = "Duplicate selected items"
toggle_handmade.short_description = "Toggle Handmade"
toggle_samplable.short_description = "Toggle SAMPLABLEs"
toggle_parent_format.short_description = "Refresh Parent Formats"
tagga_terracotta.short_description = "Tagga con terracotta"
assign_catalogue.short_description = "Assign to Catalogue 2020"


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
            kwargs["queryset"] = Tag.objects.filter(parent__slug='finish').order_by('-slug')
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
    list_display = ('name','summary','slug','in_catalogue','in_menu','in_home','in_product_edit','in_footer','public','order','parent','data_type')
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
    summernote_fields = ('content_it','content_en',)
    fields = ('title_it','title_en','content_it','content_en','publish_date','slug')
    list_display = ('title_','id','created_at','publish_date','slug','author')

    search_fields = ('title_it','title_en','slug')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

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

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

from import_export.fields import Field

class ProductResource(resources.ModelResource):
    
    title = Field()
    description = Field()
    image_link = Field()
    availability = Field()
    inventory = Field()
    condition = Field()
    price = Field()
    link = Field()
    image_link = Field()
    brand = Field()

    class Meta:
        model = EasyProductProxy
        fields = ( 'code','title', 'description','availability','inventory','condition','price','link','image_link','brand')
        export_order = ( 'code','title', 'description','availability','inventory','condition','price','link','image_link','brand')

    def dehydrate_title(self, product):
        
        if product.publication and product.publication.title and product.name:
            return '%s - %s - size: %s' % (product.publication.title,product.name,product.default_format())

    def dehydrate_description(self, product):
        return '%s' % (product.publication.content)

    def dehydrate_image_link(self, product):
        cv_img = product.cover()
        if cv_img:
            return 'https://taleoftiles.s3.amazonaws.com/%s' % (cv_img.imagefile)
        else:
            return ''

    def dehydrate_availability(self, product):
        return "available for order"

    def dehydrate_inventory(self, product):
        return "1000"

    def dehydrate_condition(self, product):
        return "new"
    
    def dehydrate_price(self, product):
        return '%s EUR' % (product.max_price(product.default_format()))

    def dehydrate_link(self, product):
        return 'https://www.taleoftiles.com/en/product/%s EUR' % (product.code)     
           
    def dehydrate_brand(self, product):
        return '%s' % (product.MPN)     

class EasyProductAdmin(ImportExportActionModelAdmin):
    
    model = EasyProductProxy
    inlines = (PriceStackedAdmin,)
    readonly_fields = ('code','tags')

    search_fields = ('name', 'code')
    list_display = ('code','name','serie','order','MPN','default_format')
    resource_class = ProductResource

    class Meta:
        proxy = True

    def default_format(self, obj):
        return "\n".join([p.size.name + '\n' for p in obj.prices.filter(default = True )])    
    
    
class ProductAdmin(admin.ModelAdmin):
    form = CustomProductModelForm
    actions = [duplicate_product,assign_catalogue]
    resource_class = ProductResource
    inlines = (PriceStackedAdmin,PhotoStackedAdmin)

    search_fields = ('name', 'code')
    
    list_display = ('name_','id',
                    'code',
                    'order',
                    'wait_time',
                    'min_ammount',
                    'is_decor',
                    'available',
                    'is_active',
                    'formats_parent_',
                    'formats_',
                    'colours_',
                    'setting_',
                    'style_',
                    'effect_',
                    'finish_',
                    'samplable_',
                    'publication',
                    'support_to',
                    'techspec',
                    )
    def name_(self, obj):
        if obj.name == " ":
            return obj.code
        return obj.name

    def tags_(self, obj):
        return "\n".join([p.name + ' * ' for p in obj.tags.all()])    
    
    def formats_(self, obj):
        return "\n".join([p.name + '\n' for p in obj.tags.filter(parent__parent__slug='format')])    
    def formats_parent_(self, obj):
        return "\n".join([p.name + '\n' for p in obj.tags.filter(parent__slug='format')])    
    def colours_(self, obj):
        return "\n".join([p.name + '\n' for p in obj.tags.filter(parent__slug='colour')])    
    def setting_(self, obj):
        return "\n".join([p.name + '\n' for p in obj.tags.filter(parent__slug='setting')])    
    def style_(self, obj):
        return "\n".join([p.name + '\n' for p in obj.tags.filter(parent__slug='style')])    
    def effect_(self, obj):
        return "\n".join([p.name + '\n' for p in obj.tags.filter(parent__slug='effect')])    
    def finish_(self, obj):
        return "\n".join([p.name + '\n' for p in obj.tags.filter(parent__slug='finish')])    
    def samplable_(self, obj):
        return "\n".join([p.name + '\n' for p in obj.tags.filter(slug='samplable')])    
    def decor_(self, obj):
        return "\n".join([p.name + '\n' for p in obj.tags.filter(slug='decor')])    
    def product_edit_(self, obj):
        return "\n".join([p.name + '\n' for p in obj.tags.filter(in_product_edit = True)])    


class TechnicalSpecAdmin(admin.ModelAdmin):
    model = TechnicalSpec
    list_display = ('slug','file','icons_',)

    def icons_(self, obj):
        return "\n".join([p.name for p in obj.icons.all()])    

admin.site.register(Tag,TagAdmin)
# admin.site.register(Tag,SerieAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(EasyProductProxy,EasyProductAdmin)

admin.site.register(Price,PriceAdmin)
admin.site.register(Publication,PublicationAdminSelf)

admin.site.register(Icon,IconAdminSelf)
admin.site.register(TechnicalSpec,TechnicalSpecAdmin)
admin.site.register(Catalogue,CatalogueAdmin)

