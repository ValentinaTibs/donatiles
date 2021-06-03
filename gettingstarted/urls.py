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
    path("",                            taleoftiles.views.index,     name="index"),

    path('catalogue/',                  taleoftiles.views.catalogue,  name="catalogue"),
    path("product/<slug:product_code>", taleoftiles.views.product,  name="product"),
    path("compute_price/",              taleoftiles.views.compute_price,  name="compute_price"),

    path("add_chart/<slug:product_code>",   CRM.views.add_chart,  name="add_chart"),
    path("del_chart/<int:item_id>",         CRM.views.del_chart,  name="del_chart"),
    path("add_sample/<slug:product_code>",  CRM.views.add_sample, name="add_sample"),
    path("ajax_add_sample",                 CRM.views.ajax_add_sample, name="ajax_add_sample"),
    
    path("del_sample/<int:item_id>",        CRM.views.del_sample, name="del_sample"),
    path("ajax_del_sample",                 CRM.views.ajax_del_sample, name="ajax_del_sample"),   

    path("add_user/",                                       CRM.views.add_user,   name="add_user"),
    path("account/",                                        CRM.views.account,    name="account"),
    path('password_reset/done/',    auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/',             auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path("accounts/password_reset/",layout.views.password_reset_request, name="password_reset"),

    path("add_sample_order", CRM.views.add_sample_order, name="add_sample_order"),
    path("add_order/<str:is_sample>", CRM.views.add_order, name="add_order"),
    path("summary/<str:id_>",  CRM.views.summary,  name="summary"),
    path("shipping/<str:id_>", CRM.views.shipping, name="shipping"),
    path("payment/<str:id_>",   CRM.views.payment,  name="payment"),
    path("order/<str:id_>",   CRM.views.order,  name="order"),
    path("ajax_pay_order",   CRM.views.ajax_pay_order,  name="ajax_pay_order"),
    

    path("blog/",                       blog.views.blog, name="blog"),
    path("blog/<slug:the_filter>/",     blog.views.blog, name="blog"),
    path('blog/post/<slug:post_slug>/', blog.views.post, name="post"),

    path("support/",        layout.views.support, name="support"),
    path("termsandconds/",  layout.views.termsandconds, name="termsandconds"),
    path("privacypolicy/",  layout.views.privacypolicy, name="privacypolicy"),

    prefix_default_language=False
)



if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
