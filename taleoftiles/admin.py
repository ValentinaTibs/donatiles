from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

from django_summernote.admin import SummernoteModelAdmin

from taleoftiles.models import  Product, Tag, Publication, Price, EasyProductProxy
from taleoftiles.models import TechnicalSpec, Catalogue
from layout.models      import Image, Icon

from taleoftiles.forms import CustomProductModelForm,UpdateScoreForm


def disable_action(modeladmin, request, queryset):
    for product in queryset:
        product.is_active = False
        product.save()

disable_action.short_description = "Disable Product"

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

from django.db.models import Q

class PriceStackedAdmin(admin.StackedInline):
    model = Price

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "size":
            Q(parent__parent__slug__in='format')
            kwargs["queryset"] = Tag.objects.filter(Q(parent__parent__slug='format') | Q(parent__slug='finish'))
        
            # if db_field.name == "finish_tag":
            # kwargs["queryset"] = Tag.objects.filter(parent__slug='finish').order_by('-slug')
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class PriceAdmin(admin.ModelAdmin):

    model = Price

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "size":
            kwargs["queryset"] = Tag.objects.filter(parent__parent__slug='format')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    list_display = ("product","size","euros","m2_box","weight_box")

class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ('name','summary','slug','in_catalogue','in_menu','in_home','in_product_edit','in_footer','public','order','parent','data_type')

    search_fields = ('name','parent__slug','parent__parent__slug' )


class SerieAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ('name','summary','slug','in_catalogue','in_menu','in_home','in_product_edit','public','parent','data_type')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Tag.objects.filter(parent__slug='serie')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PublicationAdminSelf(SummernoteModelAdmin):
    model = Publication
    summernote_fields = ('content_it','content_en','content_fr')
    fields = ('title_it','title_en','title_fr','content_it','content_en','content_fr','publish_date','slug')
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
from import_export.admin import ImportExportActionModelAdmin
from import_export.fields import Field
from django.utils.html import strip_tags

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
        return '%s' % (strip_tags(product.publication.content))

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
        def_for = product.default_format()
        if def_for:
            return '%s EUR' % (product.max_price(def_for.slug))
        return "0"

    def dehydrate_link(self, product):
        return 'https://www.taleoftiles.com/en/product/%s ' % (product.code)     
           
    def dehydrate_brand(self, product):
        return '%s' % (product.MPN)     

class EasyProductAdmin(ImportExportActionModelAdmin):
    
    model = EasyProductProxy
    inlines = (PriceStackedAdmin,)
    readonly_fields = ('code','tags')

    search_fields = ('name', 'code')
    list_display = ('code','name','serie','order','MPN','default_format','max_price')
    resource_class = ProductResource

    class Meta:
        proxy = True

    def default_format(self, obj):
        return "%s" % (obj.default_format())    
    
    def max_price(self, obj):
        def_for = obj.default_format()
        if def_for:
            return "%s" % (obj.max_price(def_for.slug))    
        else:
            return "0"

    
class ProductAdmin(admin.ModelAdmin):
    form = CustomProductModelForm
    action_form = UpdateScoreForm
    actions = [disable_action,'set_tag_action']


    resource_class = ProductResource
    inlines = (PriceStackedAdmin,PhotoStackedAdmin)

    search_fields = ( 'code',)
    
    list_display = ('name_',
                    'code',
                    'order',
                    'wait_time',
                    'min_ammount',
                    'serie',
                    'is_decor',
                    'available',
                    'is_active',
                    'formats_parent_',
                    'formats_',
                    'colours_',
                    'effect_',
                    'finish_',
                    'carta_da_parati_', 
                    'rivestimenti_',
                    'pavimenti_',
                    'superficipremium_',                   
                    'samplable_',
                    'in_home_',
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

    def carta_da_parati_(self, obj):
        if obj.tags.filter(slug='cartadaparati'):
            return True
        return False
    carta_da_parati_.boolean = True

    def rivestimenti_(self, obj):
        if obj.tags.filter(slug='rivestimenti'):
            return True
        return False
    rivestimenti_.boolean = True

    def pavimenti_(self, obj):
        if obj.tags.filter(slug='pavimenti'):
            return True
        return False
    pavimenti_.boolean = True

    def superficipremium_(self, obj):
        if obj.tags.filter(slug='superficipremium'):
            return True
        return False
    superficipremium_.boolean = True

    def samplable_(self, obj):
        return "\n".join([p.name + '\n' for p in obj.tags.filter(slug='samplable')])    
    def in_home_(self, obj):
        return "\n".join([p.name + '\n' for p in obj.tags.filter(slug='in_home')])    
    def decor_(self, obj):
        return "\n".join([p.name + '\n' for p in obj.tags.filter(slug='decor')])    
    def product_edit_(self, obj):
        return "\n".join([p.name + '\n' for p in obj.tags.filter(in_product_edit = True)])    

    def set_tag_action(self, request, queryset):
        
        hm = Tag.objects.get(slug=request.POST['tag'])
        for product in queryset:
            the_tags = product.tags.filter(pk=hm.pk) 

            if the_tags.count()>0:
                product.tags.remove(hm.pk)
            else:
                product.tags.add(hm.pk)                
            product.save()

    set_tag_action.short_description = u'Update tag of selected products'    


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

