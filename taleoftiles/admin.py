from django.contrib import admin
from django.db import models
from django_summernote.admin import SummernoteModelAdmin

# from .models import Image, Post
# tutorial_content

from .models import Post, Tag, PostRelated, Image

class PostAdmin(SummernoteModelAdmin):

    summernote_fields = ('content',)
    fieldsets = [
            ("Title/date", {'fields': ["title","content", "publish_date","image"]}),
            ("Tags", {'fields': ["related"]}),
        ]
    list_display = ('title', 'slug', "publish_date",'image','author' )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

#    'author', 'author_first_name

class ImageAdmin(admin.ModelAdmin):
    model = Image
    list_display = ('name', 'thumb_', )
    search_fields = ('name', )
    readonly_fields  = ( 'image_', )
    
admin.site.register(Image, ImageAdmin)


admin.site.register(PostRelated)
admin.site.register(Tag)
admin.site.register(Post,PostAdmin)



# class PostAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ("URL", {'fields': ["tutorial_slug"]}),
#     ]
# #     #list_display = ('title',)
#     # fields = ('custom1',)
#     # custom1 = easy.ForeignKeyAdminField('pub')
# # #    list_display = ('title', 'pub__slug', 'pub__publish_date','pub__author' )

# #     # list_display = ('pub_title', )
# #     # fields  = ('pub_title', )

# #     # def pub_title(self, obj):
# #     #     return obj.pub.title
# #     # pub_title.short_description = 'Title'
# #     # pub_title.admin_order_field = 'pub__title'

# admin.site.register(Post, PostAdmin)

# #  class PostAdmin(admin.ModelAdmin):

# #      fieldsets = [
# #         ("Title/date", {'fields': ["tutorial_title", "tutorial_published"]}),
# #         ("URL", {'fields': ["tutorial_slug"]}),
# #         ("Series", {'fields': ["tutorial_series"]}),
# #         ("Content", {"fields": ["tutorial_content"]})
# #     ]

# #     formfield_overrides = {
# #         models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
# #     }
    
# class ImageAdmin(admin.ModelAdmin):
#     model = Image
#     list_display = ('name', 'thumb_', )
#     search_fields = ('name', )
#     readonly_fields  = ( 'image_', )
    
# admin.site.register(Image, ImageAdmin)



