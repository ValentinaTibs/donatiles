from django.contrib import admin

from blog.models import Post


class PostAdmin(admin.ModelAdmin):

    #inlines = (PhotoStackedAdmin,)
    #inlines = (PublicationAdmin,ImageStackedAdmin)
    list_display = ('name','publish_date','tags', )

    def name(self, obj):
        pub = obj.publication
        return pub.title

    def publish_date(self, obj):
        return obj.publication.publish_date
            

    def tags(self, obj):
        pub = obj.publication
        return "\n".join([p.name for p in pub.tag.all()])   

    
admin.site.register(Post,PostAdmin)