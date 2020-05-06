from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

admin.autodiscover()

import taleoftiles.views
import CRM.views
import blog.views
import layout.views


urlpatterns = [ ]
i18n_patterns(*urlpatterns  , prefix_default_language = False)

urlpatterns += i18n_patterns(
    path("",                            taleoftiles.views.index,     name="index"),
    path("catalogue/",                  taleoftiles.views.catalogue, name="catalogue"),
    path("catalogue/<slug:the_filter>/",taleoftiles.views.catalogue, name="catalogue"),

    path("product/<slug:product_slug>", taleoftiles.views.product,  name="product"),

    path("add_chart/<slug:product_slug>",                   CRM.views.add_chart,  name="add_chart"),
    path("del_chart/<slug:product_slug>/<str:is_sample>",   CRM.views.del_chart,  name="del_chart"),
    path("add_sample/<slug:product_slug>",                  CRM.views.add_sample, name="add_sample"),
    path("add_user/",                                       CRM.views.add_user,   name="add_user"),
    path("account/",                                        CRM.views.account,    name="account"),

    path("summary/",            CRM.views.summary,  name="summary"),
    path("shipping/",           CRM.views.shipping, name="shipping"),
    path("payment/<int:id_>",   CRM.views.payment,  name="payment"),
    
    path("blog/",                       blog.views.blog, name="blog"),
    path("blog/<slug:the_filter>/",     blog.views.blog, name="blog"),
    path('blog/post/<slug:post_slug>/', blog.views.post, name="post"),

    path("support/",  layout.views.support, name="support"),

    # path("blog/<slug:tag_slug>",        taleoftiles.views.blog, name="blog_tag"),
    # path('blog/post/<slug:post_slug>/', taleoftiles.views.post, name="post"),

    # path("collections/",                        taleoftiles.views.collections, name="collections"),
    # path("collections/<slug:tag_slug>/",        taleoftiles.views.collections, name="collections"),    
    # path("collection/<slug:collection_slug>/",  taleoftiles.views.collection, name="collection"),

    # path("settings/",                   taleoftiles.views.settings, name="settings"),    
    # path("settings/<slug:tag_slug>",    taleoftiles.views.settings, name="settings"),    
    # path("setting/<slug:setting_slug>", taleoftiles.views.setting,  name="setting"),

    # path("products/",                   taleoftiles.views.products, name="products"),
    # path("products/<slug:tag_slug>/",   taleoftiles.views.products, name="products"),
    # path("product/<slug:product_slug>", taleoftiles.views.product,  name="product"),
    # path("product/<slug:product_slug>/add_product_chart", taleoftiles.views.add_product_chart, name="add_product_chart"),

    # path("sampler/", taleoftiles.views.sampler, name="sampler"),
    # path("sampler/del/<slug:product_id>", taleoftiles.views.del_sample, name="sampler"),

    # path("ship_sampler",    taleoftiles.views.ship_sampler, name="ship_sampler"),
    # path("ship_chart",      taleoftiles.views.ship_chart, name="ship_chart"),
    # path("shipping",        taleoftiles.views.shipping, name="shipping"),
    # path("shipping/<slug:internal_tracking_id>", taleoftiles.views.shipping, name="shipping"),

    # path("chart",           taleoftiles.views.chart,    name="chart"),   
    # path("about/",          taleoftiles.views.about,    name="about"), 
    # path("contacts/",       taleoftiles.views.contacts, name="contacts"),
    # path("askaquestion/",   taleoftiles.views.askaquestion, name="askaquestion"),
    # path("termsandcond/",   taleoftiles.views.termsandcond, name="termsandcond"),
    # url(r'^tinymce/', include('tinymce.urls')),
)

urlpatterns += (
    path("admin/", admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('accounts/', include('django.contrib.auth.urls'))
    )


if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    