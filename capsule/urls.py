from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views #import this

admin.autodiscover()

import taleoftiles.views
import CRM.views
import blog.views
import layout.views
import capsule.views


urlpatterns = [ ]
i18n_patterns(*urlpatterns  , prefix_default_language = False)

# urlpatterns += i18n_patterns(
#     #re_path(r'^catalogue/(?:(\w+)=(\w+)(\&?))*$', taleoftiles.views.catalogue, name="catalogue"),
#     path(r'^catalogue/?q=(?P<query_search>\w+)$', 'taleoftiles.views.catalogue', name='catalogue'),
# )

urlpatterns += (
    path("admin/", admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),

    )


urlpatterns += i18n_patterns(
    path("",                            blog.views.blog,     name="index"),
    
    prefix_default_language=False
)



if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
