from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

# from tinymce import urls

admin.autodiscover()

import taleoftiles.views

# To add a new path, first import the app:
# import blog

# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", taleoftiles.views.index, name="index"),
    path("blog/", taleoftiles.views.blog, name="blog"),
    path("blog/<slug:tag_slug>", taleoftiles.views.tag, name="tag"),
    path('blog/post/<slug:post_slug>/',  taleoftiles.views.post, name="post"),

    path("settings/", taleoftiles.views.settings, name="settings"),    
    path("settings/<slug:setting_slug>", taleoftiles.views.setting, name="setting"),
    
    path("product/<slug:product_slug>", taleoftiles.views.product, name="product"),

    path("collection/<slug:collection_slug>/", taleoftiles.views.collection, name="collection"),    
    
    path("admin/", admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    # url(r'^tinymce/', include('tinymce.urls')),
]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    