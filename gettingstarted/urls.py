from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

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
    path("db/", taleoftiles.views.db, name="db"),
    path("admin/", admin.site.urls),
]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    