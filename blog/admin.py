from django.contrib import admin
from layout.models import Image
from blog.models import Post


class PostImageStackedAdmin(admin.StackedInline):
    model = Image

    list_display = ('name',  )
    search_fields = ('name', )
    exclude = ('product','icon','is_cover','order','element' )


class PostAdmin(admin.ModelAdmin):
    
    model = Post

    inlines = (PostImageStackedAdmin,)
    #inlines = (PublicationAdmin,ImageStackedAdmin)
    list_display = ('name','publish_date','tags','in_home','order' )

    def name(self, obj):
        pub = obj.publication
        return pub.title

    def publish_date(self, obj):
        return obj.publication.publish_date
            
    def tags(self, obj):
        pub = obj.publication
        return "\n".join([p.name for p in pub.tag.all()])   

    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "related_products":
            kwargs["queryset"] = Product.objects.filter(is_active=True).order_by('slug')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    
admin.site.register(Post,PostAdmin)