from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

import taleoftiles.views

urlpatterns = [

    path("",taleoftiles.views.index, name="index"),
    path("blog/",taleoftiles.views.blog, name="blog"),
    path("blog/<slug:tag_slug>", taleoftiles.views.tag, name="tag"),
    path('blog/post/<slug:post_slug>/',  taleoftiles.views.post, name="post"),

    path("collection/<slug:collection_slug>/", taleoftiles.views.collection, name="collection"),    
    path("settings/", taleoftiles.views.settings, name="settings"),    
    path("settings/<slug:setting_slug>", taleoftiles.views.setting, name="setting"),
    path("product/<slug:product_slug>", taleoftiles.views.product, name="product"),

    path("sampler/<slug:session_id>", taleoftiles.views.sampler, name="sampler"),
    path("sampler/<slug:session_id>/del/<slug:product_id>", taleoftiles.views.del_sample, name="sampler"),
    path("sampler/<slug:session_id>/shipit", taleoftiles.views.ship_sampler, name="ship_sampler"),


    path("product/<slug:product_slug>/add_product_chart", taleoftiles.views.add_product_chart, name="add_product_chart"),

    path("shipping/<slug:internal_tracking_id>", taleoftiles.views.shipping, name="shipping"),

    path("about/", taleoftiles.views.about, name="about"), 
    path("askaquestion/", taleoftiles.views.askaquestion, name="askaquestion"),
    path("contacts/", taleoftiles.views.contacts, name="contacts"),
    path("termsandcond/", taleoftiles.views.termsandcond, name="termsandcond"),
    
    path("admin/", admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    # url(r'^tinymce/', include('tinymce.urls')),
]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    