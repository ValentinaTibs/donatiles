from django.contrib import admin
from .models import Image, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish_date','author' )

admin.site.register(Post, PostAdmin)


class ImageAdmin(admin.ModelAdmin):
    model = Image
    list_display = ('name', 'thumb_', )
    search_fields = ('name', )
    readonly_fields  = ( 'image_', )
    
admin.site.register(Image, ImageAdmin)



